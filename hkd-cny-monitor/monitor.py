#!/usr/bin/env python3
"""HKD/CNY exchange-rate monitor.

The monitor ranks the latest HKD -> CNY rate against a recent lookback window.
Higher CNY per HKD is better when converting Hong Kong dollars into RMB.
"""
from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover
    ZoneInfo = None  # type: ignore[assignment]


DEFAULT_CONFIG: dict[str, Any] = {
    "base": "HKD",
    "quote": "CNY",
    "amount_hkd": 100000,
    "lookback_days": 90,
    "near_high_threshold_pct": 0.30,
    "alert_min_percentile": 90,
    "target_rate": None,
    "bank_spread_pct": 0.15,
    "provider_url": "https://api.frankfurter.dev",
    "timezone": "Asia/Shanghai",
    "request_timeout_seconds": 20,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Monitor HKD/CNY and alert when the latest rate is near a recent high."
    )
    parser.add_argument("--config", default="config.json", help="Path to config JSON.")
    parser.add_argument("--output", default="data/rates.json", help="Path for result JSON.")
    parser.add_argument("--summary", default="data/summary.md", help="Path for Markdown summary.")
    parser.add_argument("--github-env", default=None, help="Optional path to GitHub Actions env file.")
    parser.add_argument(
        "--input-json",
        default=None,
        help="Read existing rate points from JSON instead of calling the exchange-rate API.",
    )
    parser.add_argument("--print-summary", action="store_true", help="Print the summary to stdout.")
    return parser.parse_args()


def load_config(path: str | Path) -> dict[str, Any]:
    config = dict(DEFAULT_CONFIG)
    config_path = Path(path)
    if config_path.exists():
        loaded = json.loads(config_path.read_text(encoding="utf-8"))
        if not isinstance(loaded, dict):
            raise ValueError(f"{config_path} must contain a JSON object")
        config.update(loaded)

    config["base"] = str(config["base"]).upper()
    config["quote"] = str(config["quote"]).upper()
    config["amount_hkd"] = float(config.get("amount_hkd") or 0)
    config["lookback_days"] = int(config.get("lookback_days") or DEFAULT_CONFIG["lookback_days"])
    config["near_high_threshold_pct"] = float(config.get("near_high_threshold_pct") or 0)
    config["alert_min_percentile"] = float(config.get("alert_min_percentile") or 0)
    config["bank_spread_pct"] = float(config.get("bank_spread_pct") or 0)
    if config.get("target_rate") in ("", None):
        config["target_rate"] = None
    else:
        config["target_rate"] = float(config["target_rate"])

    if config["base"] != "HKD" or config["quote"] != "CNY":
        raise ValueError("This monitor is configured for HKD -> CNY. Keep base=HKD and quote=CNY.")
    if config["lookback_days"] < 10:
        raise ValueError("lookback_days should be at least 10")
    if config["near_high_threshold_pct"] < 0:
        raise ValueError("near_high_threshold_pct cannot be negative")
    return config


def fetch_frankfurter_points(config: dict[str, Any]) -> tuple[list[dict[str, Any]], str]:
    today = parse_iso_date(str(config.get("end_date") or date.today().isoformat()))
    lookback_days = int(config["lookback_days"])
    buffer_days = max(45, int(lookback_days * 0.6))
    start = parse_iso_date(str(config.get("start_date") or (today - timedelta(days=lookback_days + buffer_days)).isoformat()))

    base_url = str(config["provider_url"]).rstrip("/")
    params = urlencode(
        {
            "base": config["base"],
            "quotes": config["quote"],
            "from": start.isoformat(),
            "to": today.isoformat(),
        }
    )
    url = f"{base_url}/v2/rates?{params}"
    request = Request(url, headers={"User-Agent": "hkd-cny-monitor/1.0"})
    timeout = int(config.get("request_timeout_seconds") or 20)

    try:
        with urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        raise RuntimeError(f"Exchange-rate API returned HTTP {exc.code}: {exc.reason}") from exc
    except URLError as exc:
        raise RuntimeError(f"Could not reach exchange-rate API: {exc.reason}") from exc

    points = extract_rate_points(payload, config["quote"])
    return trim_points(points, lookback_days), url


def parse_iso_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def extract_rate_points(payload: Any, quote: str) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return extract_rate_rows(payload, quote)
    if not isinstance(payload, dict):
        return []

    rates = payload.get("rates")
    points: list[dict[str, Any]] = []

    if isinstance(payload.get("value"), list):
        points.extend(extract_rate_rows(payload["value"], quote))
        return points

    if isinstance(rates, dict) and "date" in payload and quote in rates:
        points.append({"date": str(payload["date"]), "rate": float(rates[quote])})
        return points

    if isinstance(rates, dict):
        for day, quotes in rates.items():
            if isinstance(quotes, dict) and quote in quotes:
                points.append({"date": str(day), "rate": float(quotes[quote])})
            elif isinstance(quotes, (int, float)):
                points.append({"date": str(day), "rate": float(quotes)})
    elif isinstance(rates, list):
        points.extend(extract_rate_rows(rates, quote))

    return points


def extract_rate_rows(rows: list[Any], quote: str) -> list[dict[str, Any]]:
    points: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        day = row.get("date") or row.get("day")
        row_quote = str(row.get("quote") or quote).upper()
        value = row.get(quote) or row.get("rate")
        if day and value is not None and row_quote == quote:
            points.append({"date": str(day), "rate": float(value)})
    return points


def load_points_from_json(path: str | Path, quote: str) -> list[dict[str, Any]]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(payload, dict) and isinstance(payload.get("points"), list):
        return normalize_points(payload["points"])
    if isinstance(payload, dict) and "rates" in payload:
        return normalize_points(extract_rate_points(payload, quote))
    if isinstance(payload, dict) and isinstance(payload.get("value"), list):
        return normalize_points(extract_rate_points(payload, quote))
    if isinstance(payload, list):
        return normalize_points(payload)
    raise ValueError(f"Unsupported input JSON format: {path}")


def normalize_points(points: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized = []
    for point in points:
        day = str(point.get("date") or "")
        rate = float(point.get("rate"))
        if not day:
            continue
        if not math.isfinite(rate) or rate <= 0:
            continue
        normalized.append({"date": day, "rate": round(rate, 8)})
    normalized.sort(key=lambda item: item["date"])
    return normalized


def trim_points(points: list[dict[str, Any]], lookback_days: int) -> list[dict[str, Any]]:
    normalized = normalize_points(points)
    if len(normalized) < 5:
        raise RuntimeError("Not enough rate observations to analyze")
    return normalized[-lookback_days:]


def pct_change(points: list[dict[str, Any]], periods: int) -> float | None:
    if len(points) <= periods:
        return None
    previous = points[-periods - 1]["rate"]
    latest = points[-1]["rate"]
    return (latest - previous) / previous * 100


def moving_average(values: list[float], periods: int) -> float:
    window = values[-min(periods, len(values)) :]
    return statistics.fmean(window)


def analyze_points(points: list[dict[str, Any]], config: dict[str, Any], source_url: str | None = None) -> dict[str, Any]:
    points = trim_points(points, int(config["lookback_days"]))
    values = [float(point["rate"]) for point in points]
    latest = points[-1]
    latest_rate = float(latest["rate"])
    high_rate = max(values)
    low_rate = min(values)
    high_dates = [point["date"] for point in points if float(point["rate"]) == high_rate]
    low_dates = [point["date"] for point in points if float(point["rate"]) == low_rate]
    distance_to_high_pct = (high_rate - latest_rate) / high_rate * 100
    distance_from_low_pct = (latest_rate - low_rate) / low_rate * 100
    percentile = sum(1 for value in values if value <= latest_rate) / len(values) * 100
    volatility_pct = statistics.pstdev(values) / statistics.fmean(values) * 100 if len(values) > 1 else 0.0

    amount_hkd = float(config.get("amount_hkd") or 0)
    bank_spread_pct = float(config.get("bank_spread_pct") or 0)
    gross_cny = amount_hkd * latest_rate
    estimated_net_cny = gross_cny * (1 - bank_spread_pct / 100)
    missed_high_cny = amount_hkd * max(high_rate - latest_rate, 0)
    target_rate = config.get("target_rate")

    threshold_pct = float(config["near_high_threshold_pct"])
    min_percentile = float(config["alert_min_percentile"])
    near_high = distance_to_high_pct <= threshold_pct
    percentile_ok = percentile >= min_percentile
    target_hit = target_rate is not None and latest_rate >= float(target_rate)
    alert = bool(target_hit or (near_high and percentile_ok))

    if alert:
        status = "alert"
        status_label = "高位提醒"
        action = "已进入配置的近期高位区间。适合重点比较银行实盘价，并按你的资金计划考虑是否分批换汇。"
    elif distance_to_high_pct <= threshold_pct * 2 or percentile >= 80:
        status = "watch"
        status_label = "接近高位"
        action = "价格已经偏高但未完全触发提醒。可以继续观察，并提前准备好换汇渠道和限价。"
    else:
        status = "wait"
        status_label = "继续等待"
        action = "距离近期高点还有空间。非刚需时，继续等待更优报价更符合高点换汇目标。"

    latest_date = parse_iso_date(str(latest["date"]))
    last_high_date = parse_iso_date(str(high_dates[-1]))
    days_since_high = (latest_date - last_high_date).days
    generated_at = now_for_timezone(str(config.get("timezone") or "Asia/Shanghai")).isoformat(timespec="seconds")

    return {
        "schema_version": 1,
        "generated_at": generated_at,
        "source": {
            "name": "Frankfurter exchange-rate API",
            "url": source_url,
            "base": config["base"],
            "quote": config["quote"],
            "note": "Daily reference rates. Actual bank or broker quotes may differ.",
        },
        "config": {
            "amount_hkd": amount_hkd,
            "lookback_days": int(config["lookback_days"]),
            "near_high_threshold_pct": threshold_pct,
            "alert_min_percentile": min_percentile,
            "target_rate": target_rate,
            "bank_spread_pct": bank_spread_pct,
        },
        "latest": {
            "date": latest["date"],
            "rate": round(latest_rate, 8),
            "label": f"1 HKD = {latest_rate:.6f} CNY",
        },
        "window": {
            "from": points[0]["date"],
            "to": points[-1]["date"],
            "observations": len(points),
            "high_rate": round(high_rate, 8),
            "high_dates": high_dates[-5:],
            "low_rate": round(low_rate, 8),
            "low_dates": low_dates[-5:],
            "mean_rate": round(statistics.fmean(values), 8),
            "median_rate": round(statistics.median(values), 8),
            "ma_7": round(moving_average(values, 7), 8),
            "ma_30": round(moving_average(values, 30), 8),
            "change_7d_pct": round_or_none(pct_change(points, 7), 4),
            "change_30d_pct": round_or_none(pct_change(points, 30), 4),
            "volatility_pct": round(volatility_pct, 4),
            "distance_to_high_pct": round(distance_to_high_pct, 4),
            "distance_from_low_pct": round(distance_from_low_pct, 4),
            "percentile": round(percentile, 2),
            "days_since_high": days_since_high,
        },
        "amount": {
            "hkd": round(amount_hkd, 2),
            "gross_cny_at_latest": round(gross_cny, 2),
            "estimated_net_cny_after_spread": round(estimated_net_cny, 2),
            "missed_cny_vs_recent_high": round(missed_high_cny, 2),
        },
        "signals": {
            "status": status,
            "status_label": status_label,
            "alert": alert,
            "near_high": near_high,
            "percentile_ok": percentile_ok,
            "target_hit": target_hit,
            "action": action,
        },
        "points": points,
        "notes": [
            "本工具用于汇率监测和提醒，不构成投资、税务或法律建议。",
            "实际换汇请以银行、券商或持牌机构的实时买入价、手续费和额度规则为准。",
        ],
    }


def now_for_timezone(tz_name: str) -> datetime:
    if ZoneInfo is not None:
        try:
            return datetime.now(ZoneInfo(tz_name))
        except Exception:
            pass
    return datetime.now(timezone(timedelta(hours=8)))


def round_or_none(value: float | None, digits: int) -> float | None:
    return None if value is None else round(value, digits)


def fmt_pct(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value:.2f}%"


def render_summary(result: dict[str, Any]) -> str:
    latest = result["latest"]
    window = result["window"]
    amount = result["amount"]
    signals = result["signals"]
    config = result["config"]
    source = result["source"]

    lines = [
        "# HKD/CNY 汇率监测",
        "",
        f"- 信号：{signals['status_label']} ({signals['status']})",
        f"- 最新：{latest['label']}，日期 {latest['date']}",
        f"- {config['lookback_days']} 日窗口高点：{window['high_rate']:.6f}，最近高点日期 {window['high_dates'][-1]}",
        f"- 距离近期高点：{window['distance_to_high_pct']:.2f}%",
        f"- 当前分位：{window['percentile']:.2f}%，触发阈值 {config['alert_min_percentile']:.2f}%",
        f"- 7 日变化：{fmt_pct(window['change_7d_pct'])}，30 日变化：{fmt_pct(window['change_30d_pct'])}",
        f"- 估算：{amount['hkd']:,.2f} HKD 按最新参考价约 {amount['gross_cny_at_latest']:,.2f} CNY",
        f"- 距离近期高点少换：约 {amount['missed_cny_vs_recent_high']:,.2f} CNY",
        "",
        f"建议动作：{signals['action']}",
        "",
        f"数据源：{source['name']} ({source.get('url') or 'n/a'})",
        "备注：参考汇率不等于银行实盘价；真正换汇前请比较银行/券商买入价、手续费和额度规则。",
    ]
    return "\n".join(lines) + "\n"


def write_json(path: str | Path, payload: dict[str, Any]) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: str | Path, content: str) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding="utf-8")


def write_github_env(path: str | Path, result: dict[str, Any]) -> None:
    signals = result["signals"]
    latest = result["latest"]
    title = f"HKD/CNY {signals['status_label']} {latest['rate']:.6f} ({latest['date']})"
    values = {
        "HKD_CNY_ALERT": "true" if signals["alert"] else "false",
        "HKD_CNY_STATUS": signals["status"],
        "HKD_CNY_TITLE": title.replace("\n", " "),
    }
    with Path(path).open("a", encoding="utf-8") as handle:
        for key, value in values.items():
            handle.write(f"{key}={value}\n")


def main() -> int:
    args = parse_args()
    try:
        config = load_config(args.config)
        if args.input_json:
            points = trim_points(load_points_from_json(args.input_json, config["quote"]), config["lookback_days"])
            source_url = f"file:{args.input_json}"
        else:
            points, source_url = fetch_frankfurter_points(config)
        result = analyze_points(points, config, source_url)
        summary = render_summary(result)
        write_json(args.output, result)
        write_text(args.summary, summary)
        if args.github_env:
            write_github_env(args.github_env, result)
        if args.print_summary:
            print(summary)
        return 0
    except Exception as exc:
        print(f"monitor failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

# 港币兑人民币汇率监测系统

这个仓库用于监测 `HKD -> CNY`，目标是帮助你在港币换人民币时接近期内高点。系统关注的是 `1 HKD = 多少 CNY`，数值越高，港币换人民币越划算。

已部署到 `zhu-pengli.github.io` 的子目录：`https://zhu-pengli.github.io/hkd-cny-monitor/dashboard.html`。

## 功能

- 拉取 HKD/CNY 日度参考汇率。
- 计算近期高点、低点、当前分位、7 日/30 日变化。
- 判断是否进入“近期高位区间”。
- 按你的港币金额估算可换人民币，以及距离近期高点少换多少。
- 提供静态仪表盘 `dashboard.html`。
- 提供 GitHub Actions 定时监测，触发高位时自动开/更新 GitHub Issue。

## 本地运行

```powershell
cd C:\Users\18018\Documents\Codex\2026-07-09\nig\outputs\hkd-cny-monitor
python monitor.py --print-summary
python -m http.server 8000
```

然后打开：

```text
http://localhost:8000/dashboard.html
```

脚本会生成：

- `data/rates.json`：仪表盘读取的数据。
- `data/summary.md`：本次监测摘要。

运行测试：

```powershell
python -m unittest discover
```

## 配置

编辑 `config.json`：

```json
{
  "amount_hkd": 100000,
  "lookback_days": 90,
  "near_high_threshold_pct": 0.3,
  "alert_min_percentile": 90,
  "target_rate": null,
  "bank_spread_pct": 0.15
}
```

关键字段：

- `amount_hkd`：准备换出的港币金额。
- `lookback_days`：判断近期高点的窗口，默认 90 个报价日。
- `near_high_threshold_pct`：距离窗口高点多少以内算接近高点，默认 `0.3%`。
- `alert_min_percentile`：当前报价至少处于近期分位的多少以上才提醒，默认 `90%`。
- `target_rate`：你自己的心理价位，例如 `0.93`；填 `null` 则只用近期高点规则。
- `bank_spread_pct`：估算银行/券商价差，默认 `0.15%`，仅用于粗略净额估算。

## 高位提醒规则

默认触发条件：

```text
最新 HKD/CNY 距离 90 日高点 <= 0.3%
并且
当前分位 >= 90%
```

如果设置了 `target_rate`，达到心理价位也会触发提醒。

## GitHub Actions

仓库已经包含 `.github/workflows/hkd-cny-monitor.yml`。推到 GitHub 后，它会在工作日北京时间 18:15 自动运行，也可以在 Actions 页面手动运行。

```powershell
git init
git add .
git commit -m "Add HKD CNY monitor"
git branch -M main
git remote add origin https://github.com/YOUR_NAME/YOUR_REPO.git
git push -u origin main
```

如果触发高位提醒，Actions 会创建或更新一个 `HKD/CNY ...` 开头的 Issue；如果下一次没有触发，会自动关闭旧提醒。

## GitHub Pages 仪表盘

推到 GitHub 后，可以在仓库设置里启用 Pages：

```text
Settings -> Pages -> Deploy from a branch -> main / root
```

启用后访问：

```text
https://YOUR_NAME.github.io/YOUR_REPO/dashboard.html
```

## 数据源和注意事项

数据源是 [Frankfurter exchange-rate API](https://frankfurter.dev/)，适合做日度参考汇率监测。实际换汇前请以银行、券商或持牌机构的实时买入价、手续费和额度规则为准。

这个系统是监测和提醒工具，不构成投资、税务或法律建议。

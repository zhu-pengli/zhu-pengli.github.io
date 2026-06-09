---
layout: page
permalink: /publications/
title: Publications
description: 
nav: true
nav_order: 2
---

<!-- _pages/publications.md -->

<!-- Bibsearch Feature -->

{% include bib_search.liquid %}

<div class="publications">

{% bibliography %}

</div>

<script>
  document.addEventListener("DOMContentLoaded", function () {
    const linkPriority = ["Website", "DOI", "arXiv", "HTML", "PDF", "Code"];

    document.querySelectorAll(".publications > .row").forEach(function (publication) {
      const links = Array.from(publication.querySelectorAll(".links a[href]"));
      if (!links.length) return;

      const primaryLink =
        linkPriority
          .map(function (label) {
            return links.find(function (link) {
              return link.textContent.trim().toLowerCase() === label.toLowerCase();
            });
          })
          .find(Boolean) || links[0];

      const href = primaryLink.getAttribute("href");
      if (!href) return;

      const title = publication.querySelector(".title");
      if (title && !title.querySelector("a")) {
        const titleLink = document.createElement("a");
        titleLink.href = href;
        titleLink.target = "_blank";
        titleLink.rel = "external nofollow noopener";
        titleLink.style.color = "inherit";
        titleLink.style.textDecoration = "none";
        titleLink.innerHTML = title.innerHTML;
        title.replaceChildren(titleLink);
      }

      const preview = publication.querySelector(".abbr img.preview");
      if (preview && !preview.closest("a")) {
        const previewLink = document.createElement("a");
        previewLink.href = href;
        previewLink.target = "_blank";
        previewLink.rel = "external nofollow noopener";
        preview.parentNode.insertBefore(previewLink, preview);
        previewLink.appendChild(preview);
      }
    });
  });
</script>

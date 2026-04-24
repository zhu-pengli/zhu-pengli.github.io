# Pengli Zhu Homepage

This repository contains the source for <https://zhu-pengli.github.io/>.

The site is based on the al-folio Jekyll theme, with the repository kept focused on the personal homepage so it is easier to maintain.

## Common Edits

- Homepage text: `_pages/about.md`
- Publications: `_bibliography/papers.bib`
- CV page content: `_data/cv.yml`
- Social links: `_data/socials.yml`
- Profile image: `assets/img/prof_pic.png`
- Site-wide settings: `_config.yml`

## Local Preview

```bash
bundle install
bundle exec jekyll serve
```

Then open <http://localhost:4000/>.

## Deployment

The public URL remains:

<https://zhu-pengli.github.io/>

GitHub Actions builds the site when changes are pushed to `master`.

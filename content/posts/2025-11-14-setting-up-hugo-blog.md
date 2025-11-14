---
title: "Setting Up Hugo Blog"
date: 2025-11-14
draft: false
tags: ["hugo", "static-site-generator", "blog"]
---

## Summary

Today I set up a Hugo static site generator for my learning blog. Hugo is a fast, Go-based tool that converts markdown files into a complete website.

## Details

### Why Hugo?

- Single binary with no dependencies (no Ruby, no Node.js required)
- Extremely fast build times
- Simple markdown-based content
- Easy deployment to GitHub Pages

### Setup Process

1. Installed Hugo via Homebrew: `brew install hugo`
2. Initialized site: `hugo new site . --force`
3. Added PaperMod theme (clean, minimal design)
4. Configured `hugo.toml` with site settings
5. Created content structure in `content/posts/`

### Hugo Post Format

Posts in Hugo require front matter (the YAML section at the top) with:
- `title`: Post title
- `date`: Publication date
- `draft`: Whether post is published or draft
- `tags`: Optional tags for categorization

## Resources

- [Hugo Documentation](https://gohugo.io/documentation/)
- [PaperMod Theme](https://github.com/adityatelange/hugo-PaperMod)
- [Hugo Quick Start](https://gohugo.io/getting-started/quick-start/)

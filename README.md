# Rupak Learns

A simple blog for documenting weekly learnings. Built with Hugo and deployed to GitHub Pages.

## How to Add a Post

Create a new markdown file in the `content/posts/` directory:

```bash
hugo new content posts/2025-11-14-topic-name.md
```

Or manually create: `content/posts/2025-11-14-topic-name.md`

## Post Format

Each post requires Hugo front matter:

```markdown
---
title: "Title of What I Learned"
date: 2025-11-14
draft: false
tags: ["tag1", "tag2"]
---

## Summary

Quick overview of what I learned...

## Details

The meat of the content...

## Resources

- Links
- References
```

## Local Development

```bash
# Start local server (with drafts)
hugo server -D

# Build site
hugo

# View at http://localhost:1313
```

## Searching Posts

```bash
# Search by keyword
grep -r "keyword" content/posts/

# Search by date
ls content/posts/ | grep "2025-11"
```

## Deployment

Site automatically deploys to GitHub Pages via GitHub Actions when pushing to main branch.

**Live site:** https://rlamsal.github.io/rupak-learns/

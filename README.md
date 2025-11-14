# Rupak Learns

A simple blog for documenting weekly learnings.

## How to Add a Post

Create a new markdown file in the `posts/` directory:

```bash
# Using date format (recommended for chronological ordering)
posts/2025-11-14-topic-name.md

# Or just topic name
posts/learning-about-x.md
```

## Post Format

Each post should start with a basic header:

```markdown
# Title of What I Learned

**Date:** 2025-11-14

## Summary

Quick overview of what I learned...

## Details

The meat of the content...

## Resources

- Links
- References
```

## Searching Posts

```bash
# Search by keyword
grep -r "keyword" posts/

# Search by date
ls posts/ | grep "2025-11"
```

## Future Enhancements

- Add static site generator (Eleventy, Hugo, etc.)
- Deploy to GitHub Pages or Netlify
- Add tags/categories
- RSS feed

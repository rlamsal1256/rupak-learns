"""Handle markdown file operations with frontmatter."""
import os
from datetime import datetime
import frontmatter
import yaml


def save_draft(source_url, highlights, tags=None):
    """
    Save a draft note with highlights and commentary.

    Args:
        source_url: Source article URL
        highlights: List of dicts with 'quote' and 'commentary' keys
        tags: Optional list of tags

    Returns:
        Filename of saved draft
    """
    if tags is None:
        tags = []

    now = datetime.now()
    date_str = now.strftime('%Y-%m-%d')
    time_str = now.isoformat()

    # Generate slug from source URL
    slug = generate_slug(source_url)
    filename = f"{date_str}-{slug}.md"

    # Build content
    content_parts = []
    for i, highlight in enumerate(highlights, 1):
        if highlight['quote'].strip():
            content_parts.append(f"## Highlight {i}")
            content_parts.append(f"> {highlight['quote'].strip()}")
            content_parts.append("")
            if highlight['commentary'].strip():
                content_parts.append(highlight['commentary'].strip())
                content_parts.append("")

    content = "\n".join(content_parts)

    # Create frontmatter
    post = frontmatter.Post(content)
    post['source_url'] = source_url
    post['created_at'] = time_str
    post['tags'] = tags
    post['draft'] = True

    # Save to drafts directory
    filepath = os.path.join('drafts', filename)
    with open(filepath, 'w') as f:
        f.write(frontmatter.dumps(post))

    return filename


def load_draft(filename):
    """
    Load a draft note.

    Returns:
        Dict with 'metadata' and 'highlights' keys
    """
    filepath = os.path.join('drafts', filename)
    with open(filepath, 'r') as f:
        post = frontmatter.load(f)

    # Parse highlights from content
    highlights = parse_highlights(post.content)

    return {
        'metadata': post.metadata,
        'highlights': highlights,
        'filename': filename
    }


def list_drafts():
    """List all draft files with metadata."""
    drafts = []
    draft_dir = 'drafts'

    if not os.path.exists(draft_dir):
        return drafts

    for filename in os.listdir(draft_dir):
        if filename.endswith('.md'):
            filepath = os.path.join(draft_dir, filename)
            with open(filepath, 'r') as f:
                post = frontmatter.load(f)

            drafts.append({
                'filename': filename,
                'source_url': post.get('source_url', ''),
                'created_at': post.get('created_at', ''),
                'tags': post.get('tags', [])
            })

    # Sort by created_at descending
    drafts.sort(key=lambda x: x['created_at'], reverse=True)
    return drafts


def parse_highlights(content):
    """Parse markdown content into highlights list."""
    highlights = []
    lines = content.split('\n')

    current_quote = []
    current_commentary = []
    in_quote = False

    for line in lines:
        if line.startswith('## Highlight'):
            # Save previous highlight if exists
            if current_quote or current_commentary:
                highlights.append({
                    'quote': '\n'.join(current_quote).replace('> ', ''),
                    'commentary': '\n'.join(current_commentary)
                })
                current_quote = []
                current_commentary = []
            in_quote = True
        elif line.startswith('>'):
            current_quote.append(line)
            in_quote = True
        elif line.strip() == '':
            if in_quote:
                in_quote = False
        else:
            if not in_quote:
                current_commentary.append(line)

    # Save last highlight
    if current_quote or current_commentary:
        highlights.append({
            'quote': '\n'.join(current_quote).replace('> ', ''),
            'commentary': '\n'.join(current_commentary)
        })

    return highlights


def generate_slug(url):
    """Generate a URL-safe slug from a source URL."""
    import re
    from urllib.parse import urlparse

    parsed = urlparse(url)
    path = parsed.path.strip('/')

    if path:
        # Use the last path segment
        slug = path.split('/')[-1]
    else:
        # Use domain name
        slug = parsed.netloc.replace('www.', '')

    # Clean up
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    slug = slug[:50]  # Limit length

    return slug or 'note'

"""Convert draft notes to Hugo-ready blog posts."""
import os
import re
from datetime import datetime
import frontmatter


def publish_draft(filename, title=None):
    """
    Convert a draft to Hugo format and publish to content/posts/.

    Args:
        filename: Draft filename
        title: Optional title override

    Returns:
        Published filename
    """
    # Load draft
    draft_path = os.path.join('drafts', filename)
    with open(draft_path, 'r') as f:
        draft = frontmatter.load(f)

    # Generate title if not provided
    if not title:
        title = generate_title_from_url(draft.get('source_url', ''))

    # Transform content to Hugo format
    hugo_content = transform_to_hugo_content(draft.content)

    # Add source link at the end
    source_url = draft.get('source_url', '')
    if source_url:
        hugo_content += f"\n\n---\n\n**Source:** [{source_url}]({source_url})\n"

    # Create Hugo frontmatter
    created_at = draft.get('created_at', datetime.now().isoformat())
    if isinstance(created_at, str):
        try:
            dt = datetime.fromisoformat(created_at)
        except ValueError:
            dt = datetime.now()
    else:
        dt = created_at

    # Format date for Hugo (RFC3339 with timezone)
    hugo_date = dt.strftime('%Y-%m-%dT%H:%M:%S-08:00')

    # Generate description from first paragraph
    description = generate_description(hugo_content)

    # Build Hugo post
    post = frontmatter.Post(hugo_content)
    post['title'] = title
    post['date'] = hugo_date
    post['draft'] = False
    post['tags'] = draft.get('tags', [])
    post['description'] = description

    # Add custom params for source
    post['params'] = {
        'source': source_url
    }

    # Save to content/posts/
    posts_dir = os.path.join('content', 'posts')
    os.makedirs(posts_dir, exist_ok=True)

    published_path = os.path.join(posts_dir, filename)
    with open(published_path, 'w') as f:
        f.write(frontmatter.dumps(post))

    return filename


def transform_to_hugo_content(draft_content):
    """
    Transform draft format to Hugo-friendly format.

    Converts:
    ## Highlight 1
    > Quote text

    Commentary text

    To:
    ## Section Title

    > Quote text

    **My thoughts:** Commentary text
    """
    lines = draft_content.split('\n')
    hugo_lines = []
    section_count = 1
    current_section_title = None
    in_quote = False
    quote_buffer = []
    commentary_buffer = []

    for i, line in enumerate(lines):
        if line.startswith('## Highlight'):
            # Flush previous section
            if quote_buffer or commentary_buffer:
                if current_section_title:
                    hugo_lines.append(current_section_title)
                    hugo_lines.append('')

                if quote_buffer:
                    hugo_lines.extend(quote_buffer)
                    hugo_lines.append('')

                if commentary_buffer:
                    hugo_lines.append(f"**My thoughts:** {commentary_buffer[0]}")
                    hugo_lines.extend(commentary_buffer[1:])
                    hugo_lines.append('')

                hugo_lines.append('---')
                hugo_lines.append('')

                quote_buffer = []
                commentary_buffer = []

            current_section_title = f"## Key Insight {section_count}"
            section_count += 1
            in_quote = False

        elif line.startswith('>'):
            quote_buffer.append(line)
            in_quote = True

        elif line.strip() == '':
            if in_quote:
                in_quote = False

        else:
            if not in_quote and line.strip():
                commentary_buffer.append(line)

    # Flush last section
    if quote_buffer or commentary_buffer:
        if current_section_title:
            hugo_lines.append(current_section_title)
            hugo_lines.append('')

        if quote_buffer:
            hugo_lines.extend(quote_buffer)
            hugo_lines.append('')

        if commentary_buffer:
            hugo_lines.append(f"**My thoughts:** {commentary_buffer[0]}")
            hugo_lines.extend(commentary_buffer[1:])

    return '\n'.join(hugo_lines).strip()


def generate_title_from_url(url):
    """Generate a readable title from source URL."""
    from urllib.parse import urlparse

    parsed = urlparse(url)
    path = parsed.path.strip('/')

    if path:
        slug = path.split('/')[-1]
    else:
        slug = parsed.netloc.replace('www.', '')

    # Convert slug to title
    title = slug.replace('-', ' ').replace('_', ' ')
    title = re.sub(r'[^\w\s]', '', title)
    title = ' '.join(word.capitalize() for word in title.split())

    return title or 'Learning Notes'


def generate_description(content):
    """Extract first meaningful paragraph as description."""
    lines = content.split('\n')

    for line in lines:
        line = line.strip()
        # Skip empty lines, headings, quotes
        if line and not line.startswith('#') and not line.startswith('>') and not line.startswith('**'):
            # Clean up markdown
            desc = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', line)  # Remove links
            desc = re.sub(r'\*\*([^\*]+)\*\*', r'\1', desc)  # Remove bold
            desc = re.sub(r'\*([^\*]+)\*', r'\1', desc)  # Remove italic
            # Truncate if too long
            if len(desc) > 160:
                desc = desc[:157] + '...'
            return desc

    return 'Notes and insights from recent learning'

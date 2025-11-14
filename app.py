"""Flask app for note-taking and blog writing."""
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from markdown import markdown
from utils.markdown_handler import save_draft, load_draft, list_drafts
from utils.hugo_converter import publish_draft, transform_to_hugo_content

app = Flask(__name__)
app.secret_key = 'dev-secret-key-change-in-production'


@app.route('/')
def index():
    """List all drafts."""
    drafts = list_drafts()
    return render_template('index.html', drafts=drafts)


@app.route('/new', methods=['GET', 'POST'])
def new_note():
    """Create a new note."""
    if request.method == 'POST':
        source_url = request.form.get('source_url', '').strip()
        if not source_url:
            flash('Source URL is required', 'error')
            return redirect(url_for('new_note'))

        # Collect highlights
        highlights = []
        i = 0
        while True:
            quote_key = f'quote_{i}'
            commentary_key = f'commentary_{i}'

            if quote_key not in request.form:
                break

            quote = request.form.get(quote_key, '').strip()
            commentary = request.form.get(commentary_key, '').strip()

            if quote or commentary:
                highlights.append({
                    'quote': quote,
                    'commentary': commentary
                })

            i += 1

        if not highlights:
            flash('Add at least one highlight or commentary', 'error')
            return redirect(url_for('new_note'))

        # Save draft
        filename = save_draft(source_url, highlights)
        flash(f'Draft saved: {filename}', 'success')
        return redirect(url_for('index'))

    return render_template('capture.html')


@app.route('/edit/<filename>', methods=['GET', 'POST'])
def edit_note(filename):
    """Edit an existing draft."""
    if request.method == 'POST':
        source_url = request.form.get('source_url', '').strip()
        if not source_url:
            flash('Source URL is required', 'error')
            return redirect(url_for('edit_note', filename=filename))

        # Collect highlights
        highlights = []
        i = 0
        while True:
            quote_key = f'quote_{i}'
            commentary_key = f'commentary_{i}'

            if quote_key not in request.form:
                break

            quote = request.form.get(quote_key, '').strip()
            commentary = request.form.get(commentary_key, '').strip()

            if quote or commentary:
                highlights.append({
                    'quote': quote,
                    'commentary': commentary
                })

            i += 1

        if not highlights:
            flash('Add at least one highlight or commentary', 'error')
            return redirect(url_for('edit_note', filename=filename))

        # Save draft (will overwrite with same filename)
        os.remove(os.path.join('drafts', filename))
        new_filename = save_draft(source_url, highlights)
        flash(f'Draft updated: {new_filename}', 'success')
        return redirect(url_for('index'))

    # Load existing draft
    draft = load_draft(filename)
    return render_template('edit.html', draft=draft)


@app.route('/preview/<filename>')
def preview_note(filename):
    """Preview a draft as it will appear when published."""
    draft = load_draft(filename)

    # Load raw content from draft file
    draft_path = os.path.join('drafts', filename)
    import frontmatter
    with open(draft_path, 'r') as f:
        draft_post = frontmatter.load(f)

    # Transform to Hugo format
    hugo_content = transform_to_hugo_content(draft_post.content)

    # Add source link
    source_url = draft_post.get('source_url', '')
    if source_url:
        hugo_content += f"\n\n---\n\n**Source:** [{source_url}]({source_url})\n"

    # Render markdown to HTML
    html_content = markdown(hugo_content, extensions=['fenced_code', 'tables', 'nl2br'])

    return render_template('preview.html',
                         draft=draft,
                         html_content=html_content,
                         filename=filename)


@app.route('/publish/<filename>', methods=['POST'])
def publish_note(filename):
    """Publish a draft to Hugo posts."""
    title = request.form.get('title', '').strip()

    try:
        published_filename = publish_draft(filename, title or None)
        flash(f'Published: {published_filename}', 'success')

        # Delete draft after publishing
        draft_path = os.path.join('drafts', filename)
        if os.path.exists(draft_path):
            os.remove(draft_path)

    except Exception as e:
        flash(f'Error publishing: {str(e)}', 'error')
        return redirect(url_for('preview_note', filename=filename))

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=5001)

// Dynamic form management for adding/removing highlights

// Initialize highlight count
if (typeof highlightCount === 'undefined') {
    highlightCount = 1;
}

document.addEventListener('DOMContentLoaded', function() {
    const addHighlightBtn = document.getElementById('addHighlight');
    const highlightsContainer = document.getElementById('highlights');

    // Add new highlight section
    addHighlightBtn.addEventListener('click', function() {
        const newSection = createHighlightSection(highlightCount);
        highlightsContainer.appendChild(newSection);
        highlightCount++;
    });

    // Handle remove buttons for existing sections (in edit mode)
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('remove-highlight')) {
            e.preventDefault();
            const section = e.target.closest('.highlight-section');
            if (section) {
                section.remove();
            }
        }
    });
});

function createHighlightSection(index) {
    const section = document.createElement('div');
    section.className = 'highlight-section';

    section.innerHTML = `
        <h3>Highlight ${index + 1}</h3>
        <div class="form-group">
            <label for="quote_${index}">Quote / Highlight</label>
            <textarea id="quote_${index}" name="quote_${index}" rows="4"
                      placeholder="Paste the quote or highlight here..."></textarea>
        </div>
        <div class="form-group">
            <label for="commentary_${index}">Your Commentary</label>
            <textarea id="commentary_${index}" name="commentary_${index}" rows="4"
                      placeholder="Add your thoughts, analysis, or notes..."></textarea>
        </div>
        <button type="button" class="btn btn-danger btn-small remove-highlight">
            Remove
        </button>
    `;

    return section;
}

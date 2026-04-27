function updateTocPreview() {
    const preview = document.getElementById('toc-preview');
    const { tocItems, tocSubitems } = collectTocData();

    if (tocItems.length === 0) {
        preview.innerHTML = '<div class="empty-toc">Нет данных для предпросмотра</div>';
        return;
    }

    let previewHTML = '';

    tocItems.forEach(item => {
        previewHTML += `
            <div class="toc-preview-item main-item">
                <div class="toc-preview-title">${item.id}. ${item.title}</div>
                <div class="toc-preview-page">${item.page}</div>
            </div>
        `;

        if (tocSubitems[item.id]) {
            tocSubitems[item.id].forEach(subitem => {
                previewHTML += `
                    <div class="toc-preview-item subitem">
                        <div class="toc-preview-title">${subitem.title}</div>
                        <div class="toc-preview-page">${subitem.page}</div>
                    </div>
                `;
            });
        }
    });

    preview.innerHTML = previewHTML || '<div class="empty-toc">Нет данных для предпросмотра</div>';
}

document.getElementById('discipline_name').addEventListener('input', function(e) {
    document.getElementById('preview-name').textContent = e.target.value || 'Название дисциплины';
});

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('expand-all').addEventListener('click', expandAll);
    document.getElementById('collapse-all').addEventListener('click', collapseAll);

    document.querySelectorAll('input').forEach(input => {
        input.addEventListener('input', updateTocPreview);
    });

    updateTocPreview();
});

document.getElementById('rpd-form').addEventListener('submit', async function(e) {
    e.preventDefault();

    const formData = new FormData(this);
    const data = Object.fromEntries(formData.entries());

    const tocData = collectTocData();
    data.toc_items = tocData.tocItems;
    data.toc_subitems = tocData.tocSubitems;

    const button = this.querySelector('.btn-generate');
    const originalText = button.querySelector('.btn-text').textContent;
    button.querySelector('.btn-text').textContent = 'Создаём документ...';
    button.disabled = true;

    try {
        const response = await fetch('/generate-word', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (!response.ok) throw new Error('Ошибка сервера: ' + response.status);

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;

        const contentDisposition = response.headers.get('Content-Disposition');
        let filename = 'РПД.docx';
        if (contentDisposition) {
            const match = contentDisposition.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/);
            if (match && match[1]) filename = match[1].replace(/['"]/g, '');
        }

        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
        alert('Документ успешно создан и скачан!');
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Ошибка при создании документа: ' + error.message);
    } finally {
        button.querySelector('.btn-text').textContent = originalText;
        button.disabled = false;
    }
});

document.getElementById('confirm-toc-btn').addEventListener('click', function() {
    const items = [];

        document.querySelectorAll('.toc-main-item').forEach((item) => {
            const itemId = item.getAttribute('data-id');
            const titleInput = item.querySelector('.toc-title');
            const pageInput = item.querySelector('.toc-page');

            if (titleInput && pageInput) {
                items.push({
                    id: itemId,
                    title: titleInput.value,
                    page: pageInput.value,
                    content: ''
                });
            }
        });

        const hasV = items.some(i => i.id === 'V');
        if (!hasV) {
            const vItem = document.querySelector('.toc-main-item[data-id="V"]');
            if (vItem) {
                const titleInput = vItem.querySelector('.toc-title');
                const pageInput = vItem.querySelector('.toc-page');
                if (titleInput && pageInput) {
                    items.push({
                        id: 'V',
                        title: titleInput.value,
                        page: pageInput.value,
                        content: ''
                    });
                }
            }
        }

    currentTocItems = items;

    document.getElementById('rpd-form').style.display = 'none';
    document.querySelector('.preview').style.display = 'none';
    document.getElementById('edit-page').style.display = 'block';

    renderEditFields();
});

document.getElementById('back-to-form-btn').addEventListener('click', function() {
    document.getElementById('rpd-form').style.display = 'block';
    document.querySelector('.preview').style.display = 'block';
    document.getElementById('edit-page').style.display = 'none';
});

document.getElementById('save-all-btn').addEventListener('click', async function() {
    const formData = new FormData(document.getElementById('rpd-form'));
    const data = Object.fromEntries(formData.entries());

    const customFilenameInput = document.getElementById('custom_filename');
    if (customFilenameInput) data.custom_filename = customFilenameInput.value;

    const tocData = collectTocData();
    data.toc_items = tocData.tocItems;
    data.toc_subitems = tocData.tocSubitems;

    data.section_contents = {};
    currentTocItems.forEach((item, index) => {
        if (item.id === 'I' || item.id === 'II') {
            const textarea = document.getElementById(`content_${index}`);
            if (textarea) data.section_contents[item.id] = textarea.value;
        } else if (item.id === 'III') {
            const descTextarea = document.getElementById('section3_desc');
            if (descTextarea) data.section_contents['III_desc'] = descTextarea.value;

            const competencies = [];
            document.querySelectorAll('#competencies-container .competence-item').forEach(compItem => {
                const competence = compItem.querySelector('.competence-field')?.value || '';
                const indicator = compItem.querySelector('.indicator-field')?.value || '';
                const results = compItem.querySelector('.results-field')?.value || '';
                if (competence || indicator || results) {
                    competencies.push({ competence, indicator, results });
                }
            });
            data.section_contents['III_competencies'] = competencies;
        }
    });

    data.credits = document.getElementById('iv_credits')?.value || '5';
    data.total_hours = document.getElementById('iv_hours')?.value || '180';
    data.attestation_form = document.getElementById('iv_attestation')?.value || 'зачёт';
    data.section_contents['IV_table'] = collectTable41Data();
    data.section_contents['IV_table42'] = collectTable42Data();

    data.section_contents['V_main_literature'] = document.getElementById('main_literature')?.value || '';
    data.section_contents['V_additional_literature'] = document.getElementById('additional_literature')?.value || '';
    data.section_contents['V_internet_resources'] = document.getElementById('internet_resources')?.value || '';

    data.section_contents['VI_table'] = collectTableVIData();
    data.section_contents['VI_description'] = document.getElementById('vi_description')?.value || 'При реализации дисциплины используются следующие помещения, оборудование и программное обеспечение:';

    data.section_contents['VII'] = document.getElementById('vii_content')?.value || '';

    data.section_contents['VIII_table'] = collectTableVIIIData();
    data.section_contents['VIII_labs'] = collectLabsData();

    data.section_contents['IX'] = document.getElementById('ix_text')?.value || '';

    const button = this;
    const originalText = button.innerHTML;
    button.disabled = true;

    try {
        const response = await fetch('/generate-word', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (!response.ok) throw new Error('Ошибка сервера: ' + response.status);

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;

        const contentDisposition = response.headers.get('Content-Disposition');
        let filename = 'РПД.docx';
        if (contentDisposition) {
            const match = contentDisposition.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/);
            if (match && match[1]) filename = match[1].replace(/['"]/g, '');
        }

        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
        alert('Документ успешно создан и скачан!');
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Ошибка при создании документа: ' + error.message);
    } finally {
        button.innerHTML = originalText;
        button.disabled = false;
    }
});

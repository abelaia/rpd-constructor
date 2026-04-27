const subitemCounters = {
    'IV': 1,
    'V': 1,
    'VIII': 1
};

function toggleSubitems(sectionId) {
    const container = document.getElementById(`subitems-${sectionId}`);
    const toggleBtn = document.querySelector(`.toc-main-item[data-id="${sectionId}"] .toggle-subitems`);

    if (container.style.display === 'none') {
        container.style.display = 'block';
        toggleBtn.textContent = '▼';
    } else {
        container.style.display = 'none';
        toggleBtn.textContent = '▶';
    }
    updateTocPreview();
}

function renumberSubitems(sectionId) {
    const container = document.getElementById(`subitems-${sectionId}`);
    const subitems = container.querySelectorAll('.subitem');

    subitems.forEach((subitem, idx) => {
        subitem.setAttribute('data-index', idx);

        const numberSpan = subitem.querySelector('.subitem-number');
        let prefix = '';
        if (sectionId === 'IV') prefix = '4';
        else if (sectionId === 'V') prefix = '5';
        else if (sectionId === 'VIII') prefix = '8';

        numberSpan.textContent = `${prefix}.${idx + 1}`;
    });

    subitemCounters[sectionId] = subitems.length;
}

function addSubitem(sectionId) {
    const container = document.getElementById(`subitems-${sectionId}`);
    const subitemsContainer = container.querySelector('.subitem-actions');
    const actionsContainer = subitemsContainer || container.querySelector('.subitem-actions');

    if (!actionsContainer) return;

    const currentSubitems = container.querySelectorAll('.subitem');
    const newIndex = currentSubitems.length;

    let prefix = '';
    if (sectionId === 'IV') prefix = '4';
    else if (sectionId === 'V') prefix = '5';
    else if (sectionId === 'VIII') prefix = '8';

    const newNumber = `${prefix}.${newIndex + 1}`;

    const newSubitem = document.createElement('div');
    newSubitem.className = 'subitem';
    newSubitem.setAttribute('data-index', newIndex);

    newSubitem.innerHTML = `
        <span class="subitem-number">${newNumber}</span>
        <input type="text" class="subitem-title" placeholder="Название подпункта" value="">
        <input type="text" class="subitem-page" placeholder="Страница" value="">
        <button type="button" class="remove-subitem-btn" onclick="removeSubitem('${sectionId}', ${newIndex})">×</button>
    `;

    actionsContainer.parentNode.insertBefore(newSubitem, actionsContainer);

    newSubitem.querySelectorAll('input').forEach(input => {
        input.addEventListener('input', updateTocPreview);
    });

    renumberSubitems(sectionId);
    updateTocPreview();
}

function removeSubitem(sectionId, index) {
    const subitem = document.querySelector(`#subitems-${sectionId} .subitem[data-index="${index}"]`);
    if (subitem && confirm('Удалить этот подпункт?')) {
        subitem.remove();
        renumberSubitems(sectionId);
        updateTocPreview();
    }
}

function expandAll() {
    document.querySelectorAll('.subitems-container').forEach(container => {
        container.style.display = 'block';
    });
    document.querySelectorAll('.toggle-subitems').forEach(btn => {
        btn.textContent = '▼';
    });
}

function collapseAll() {
    document.querySelectorAll('.subitems-container').forEach(container => {
        container.style.display = 'none';
    });
    document.querySelectorAll('.toggle-subitems').forEach(btn => {
        btn.textContent = '▶';
    });
}

function collectTocData() {
    const tocItems = [];
    const tocSubitems = {};

    document.querySelectorAll('.toc-main-item').forEach(item => {
        const itemId = item.getAttribute('data-id');
        const titleInput = item.querySelector('.toc-title');
        const pageInput = item.querySelector('.toc-page');

        if (titleInput && pageInput) {
            tocItems.push({
                id: itemId,
                title: titleInput.value,
                page: pageInput.value
            });

            const subitemsContainer = document.getElementById(`subitems-${itemId}`);
            if (subitemsContainer) {
                const subitems = [];
                subitemsContainer.querySelectorAll('.subitem').forEach(subitem => {
                    const subTitleInput = subitem.querySelector('.subitem-title');
                    const subPageInput = subitem.querySelector('.subitem-page');
                    const subNumberSpan = subitem.querySelector('.subitem-number');

                    if (subTitleInput && subPageInput && subTitleInput.value) {
                        subitems.push({
                            title: (subNumberSpan ? subNumberSpan.textContent.trim() + ' ' : '') + subTitleInput.value,
                            page: subPageInput.value
                        });
                    }
                });
                if (subitems.length > 0) tocSubitems[itemId] = subitems;
            }
        }
    });
    return { tocItems, tocSubitems };
}

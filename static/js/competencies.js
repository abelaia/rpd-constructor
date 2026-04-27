function addCompetence() {
    const container = document.getElementById('competencies-container');
    const newComp = document.createElement('div');
    newComp.className = 'competence-item';
    newComp.innerHTML = `
        <input
            type="text"
            class="competence-field"
            placeholder="Компетенция"
            value=""
        >
        <input
            type="text"
            class="indicator-field"
            placeholder="Индикатор"
            value=""
        >
        <textarea
            class="results-field"
            rows="4"
            placeholder="Результаты обучения (Знания, Умения, Навыки)"
        >
        </textarea>
        <button
            type="button"
            class="remove-competence-btn"
            onclick="removeCompetence(this)"
        >
            x
        </button>
    `;
    container.appendChild(newComp);
}

function removeCompetence(btn) {
    if (confirm('Удалить эту компетенцию?')) {
        btn.parentElement.remove();
    }
}

function collectCompetenciesData() {
    const competencies = [];
    document.querySelectorAll('#competencies-container .competence-item').forEach(compItem => {
        const competence = compItem.querySelector('.competence-field')?.value || '';
        const indicator = compItem.querySelector('.indicator-field')?.value || '';
        const results = compItem.querySelector('.results-field')?.value || '';
        if (competence || indicator || results) {
            competencies.push({ competence, indicator, results });
        }
    });
    return competencies;
}

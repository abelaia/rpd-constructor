let currentTocItems = [];

function renderEditFields() {
    const container = document.getElementById('edit-container');
    container.innerHTML = '';

    currentTocItems.forEach((item, index) => {
        if (item.id === 'I' || item.id === 'II' || item.id === 'III' || item.id === 'IV' || item.id === 'V' || item.id === 'VI' || item.id === 'VII' || item.id === 'VIII' || item.id === 'IX') {
            const editItem = document.createElement('div');
            editItem.className = 'edit-item';

            if (item.id === 'I') {
                editItem.innerHTML = `
                    <div class="edit-item-header">
                        <h3>I. ЦЕЛИ И ЗАДАЧИ ОСВОЕНИЯ ДИСЦИПЛИНЫ</h3>
                        <span class="edit-page">Стр. ${item.page}</span>
                    </div>
                    <div class="edit-item-content">
                        <label for="content_${index}">Текст раздела:</label>
                        <textarea
                            id="content_${index}"
                            class="edit-textarea"
                            rows="12"
                            placeholder="Введите цели и задачи дисциплины..."
                        >
                            ${item.content || ''}
                        </textarea>
                    </div>
                `;
            } else if (item.id === 'II') {
                editItem.innerHTML = `
                    <div class="edit-item-header">
                        <h3>II. МЕСТО ДИСЦИПЛИНЫ В СТРУКТУРЕ ОБРАЗОВАТЕЛЬНОЙ ПРОГРАММЫ</h3>
                        <span class="edit-page">Стр. ${item.page}</span>
                    </div>
                    <div class="edit-item-content">
                        <label for="content_${index}">Текст раздела:</label>
                        <textarea
                            id="content_${index}"
                            class="edit-textarea"
                            rows="12"
                            placeholder="Введите место дисциплины в учебном плане..."
                        >
                            ${item.content || ''}
                        </textarea>
                    </div>
                `;
            } else if (item.id === 'III') {
                editItem.innerHTML = `
                    <div class="edit-item-header">
                        <h3>III. ТРЕБОВАНИЯ К РЕЗУЛЬТАТАМ ОСВОЕНИЯ ДИСЦИПЛИНЫ</h3>
                        <span class="edit-page">Стр. ${item.page}</span>
                    </div>
                    <div class="edit-item-content horizontal-section">
                        <label>Описание раздела:</label>
                        <textarea
                            id="section3_desc"
                            class="edit-textarea"
                            rows="3"
                            placeholder="Освоение дисциплины направлено на формирование следующих компетенций..."
                        >
                        </textarea>
                        <label style="margin-top: 20px;">Компетенции (можно добавить несколько):</label>
                        <div id="competencies-container">
                            <div class="competence-item">
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
                                    placeholder="Результаты обучения..."
                                >
                                </textarea>
                                <button
                                    type="button"
                                    class="remove-competence-btn"
                                    onclick="removeCompetence(this)"
                                >
                                    x
                                </button>
                            </div>
                        </div>
                        <button
                            type="button"
                            class="add-competence-btn"
                            onclick="addCompetence()"
                        >
                            Добавить компетенцию
                        </button>
                    </div>
                `;
            } else if (item.id === 'IV') {
                editItem.innerHTML = `
                    <div class="edit-item-header">
                        <h3>IV. СОДЕРЖАНИЕ И СТРУКТУРА ДИСЦИПЛИНЫ</h3>
                        <span class="edit-page">Стр. ${item.page}</span>
                    </div>
                    <div class="edit-item-content">
                        <div style="display: flex; gap: 20px; flex-wrap: wrap; margin-bottom: 20px;">
                            <div>
                                <label>
                                    Трудоемкость (ЗЕ):
                                </label>
                                <input
                                    type="number"
                                    id="iv_credits"
                                    class="form-input"
                                    value="5"
                                    style="width: 100px;"
                                >
                            </div>
                            <div>
                                <label>
                                    Часов всего:
                                </label>
                                <input
                                     type="number"
                                     id="iv_hours"
                                     class="form-input"
                                     value="180"
                                     style="width: 100px;"
                                 >
                             </div>
                            <div>
                                <label>
                                    Форма аттестации:
                                </label>
                                <select
                                    id="iv_attestation"
                                    class="form-input"
                                    style="width: 150px;"
                                >
                                    <option
                                        value="зачёт"
                                    >
                                        зачёт
                                    </option>
                                    <option
                                        value="экзамен"
                                    >
                                        экзамен
                                    </option>
                                    <option
                                        value="зачёт с оценкой"
                                    >
                                        зачёт с оценкой
                                    </option>
                                </select>
                            </div>
                        </div>
                        <label>Таблица 4.1 - Содержание дисциплины по темам:</label>
                        <div id="table-41-container" style="overflow-x: auto;">
                            <table class="data-table" id="table-41">
                                <thead>
                                    <tr>
                                        <th style="width:50px">
                                            №
                                        </th>
                                        <th style="min-width:200px">
                                            Тема занятия
                                        </th>
                                        <th style="width:60px">
                                            Лекции
                                        </th>
                                        <th style="width:60px">
                                            Практич.
                                        </th>
                                        <th style="width:60px">
                                            Лабор.
                                        </th>
                                        <th style="width:60px">
                                            Конс.
                                        </th>
                                        <th style="width:70px">
                                            Сам. раб.
                                        </th>
                                        <th style="min-width:150px">
                                            Формат
                                        </th>
                                        <th style="min-width:150px">
                                            Оценочное средство
                                        </th>
                                        <th style="min-width:150px">
                                            Вид контроля
                                        </th>
                                        <th style="width:60px">
                                            Баллы
                                        </th>
                                        <th style="width:40px">
                                        </th>
                                    </tr>
                                </thead>
                                <tbody id="table-41-body">
                                    ...
                                </tbody>
                            </table>
                        </div>
                        <button type="button" class="add-row-btn" onclick="addTableRow()">+ Добавить строку в таблицу 4.1</button>
                        <label style="margin-top:30px">Таблица 4.2 - План внеаудиторной самостоятельной работы:</label>
                        <div id="table-42-container" style="overflow-x:auto">
                            <table class="data-table" id="table-42">
                                <thead>
                                    <tr>
                                        <th style="width:50px">
                                            №
                                        </th>
                                        <th style="min-width:200px">
                                            Тема занятия
                                        </th>
                                        <th style="width:70px">
                                            Семестр
                                        </th>
                                        <th style="width:80px">
                                            Сроки (нед.)
                                        </th>
                                        <th style="min-width:250px">
                                            Вид самостоятельной работы
                                        </th><th style="width:80px">
                                            Часы
                                        </th>
                                        <th style="min-width:150px">
                                            Учебно-метод. обеспечение
                                        </th>
                                        <th style="width:40px">
                                        </th>
                                    </tr>
                                </thead>
                                <tbody id="table-42-body">
                                    ...
                                </tbody>
                            </table>
                        </div>
                        <button type="button" class="add-row-btn" onclick="addTable42Row()">+ Добавить строку</button>
                    </div>
                `;
            } else if (item.id === 'V') {
                editItem.innerHTML = `
                    <div class="edit-item-header">
                        <h3>V. УЧЕБНО-МЕТОДИЧЕСКОЕ ОБЕСПЕЧЕНИЕ ДИСЦИПЛИНЫ</h3>
                        <span class="edit-page">Стр. ${item.page}</span>
                    </div>
                    <div class="edit-item-content">
                        <label>5.1. Основная литература:</label>
                        <textarea id="main_literature" class="edit-textarea" rows="6" placeholder="Пример:
                            1. Уоллс, К. Spring в действии / К. Уоллс ; пер. с англ. С. А. Витера. – 6-е изд.
                             – Москва : Диалектика, 2022. – 592 с. – ISBN 978-5-907496-12-7.
                            2. Тёрнквист, Г. Л. Изучаем Spring Boot 3.0 / Г. Л. Тёрнквист ; пер. с англ. А. А. Слинкина.
                             – Москва : ДМК Пресс, 2023. – 342 с. – ISBN 978-5-93700-145-2."
                        >
                        </textarea>
                        <label style="margin-top: 20px;">5.2. Дополнительная литература:</label>
                        <textarea id="additional_literature" class="edit-textarea" rows="4" placeholder="Пример:
                            4. Walls, C. Spring Boot in Action / C. Walls. – 5th ed. – Shelter Island :
                             Manning Publications, 2023. – 456 p. – ISBN 978-1-61729-961-2."
                        >
                        </textarea>
                        <label style="margin-top: 20px;">5.3. Перечень ресурсов сети Интернет:</label>
                        <textarea id="internet_resources" class="edit-textarea" rows="4" placeholder="Пример:
                            6. Spring Boot Fundamentals [Видеокурс] / Pluralsight. – 2023.
                             – Режим доступа: https://www.pluralsight.com/courses/spring-boot-fundamentals (дата обращения: 15.03.2024)."
                        >
                        </textarea>
                    </div>
                `;
            } else if (item.id === 'VI') {
                editItem.innerHTML = `
                    <div class="edit-item-header">
                        <h3>VI. МАТЕРИАЛЬНО-ТЕХНИЧЕСКОЕ ОБЕСПЕЧЕНИЕ ДИСЦИПЛИНЫ</h3>
                        <span class="edit-page">Стр. ${item.page}</span>
                    </div>
                    <div class="edit-item-content">
                        <label>Описание раздела:</label>
                        <textarea
                             id="vi_description"
                             class="edit-textarea"
                             rows="2"
                             placeholder="При реализации дисциплины используются следующие помещения, оборудование и программное обеспечение:"
                        >
                        При реализации дисциплины используются следующие помещения, оборудование и программное обеспечение:
                        </textarea>
                        <label>Таблица 6.1 - Материально-техническое обеспечение:</label>
                        <div id="table-vi-container">
                            <table class="table-vi-editor">
                                <thead>
                                    <tr>
                                        <th style="width: 50px;">№ п/п</th>
                                        <th>Тип аудиторного занятия</th>
                                        <th>Рекомендуемая аудитория</th>
                                        <th>Оснащение</th>
                                        <th style="width: 40px;"></th>
                                    </tr>
                                </thead>
                                <tbody id="table-vi-body">
                                    <tr>
                                        <td>
                                            <input
                                                type="text"
                                                class="vi-num"
                                                value="1"
                                            >
                                        </td>
                                        <td>
                                            <input
                                                type="text"
                                                class="vi-type"
                                                placeholder="Лекционные занятия"
                                            >
                                        </td>
                                        <td>
                                            <input
                                                type="text"
                                                class="vi-audience"
                                                placeholder="аудитория лекционного типа"
                                            >
                                            </td>
                                        <td>
                                            <textarea
                                                class="vi-equipment"
                                                rows="2"
                                                placeholder="– доска интерактивная - 1 шт., Компьютер преподавателя - 1 шт.;&#10;– Microsoft Windows, Microsoft Office PowerPoint"
                                            >
                                            </textarea>
                                        </td>
                                        <td>
                                            <button
                                                type="button"
                                                class="remove-vi-row"
                                                onclick="removeVIRow(this)"
                                            >
                                                x
                                            </button>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            <input
                                                type="text"
                                                class="vi-num"
                                                value="2"
                                            >
                                        </td>
                                        <td>
                                            <input
                                                type="text"
                                                class="vi-type"
                                                placeholder="Лабораторные занятия"
                                            >
                                            </td>
                                        <td>
                                            <input
                                                type="text"
                                                class="vi-audience"
                                                placeholder="аудитория, оснащённая персональными компьютерами"
                                            >
                                        </td>
                                        <td>
                                            <textarea
                                                class="vi-equipment"
                                                rows="2"
                                                placeholder="компьютер для студентов – 25 шт. с выходом в сеть интернет и установленной IntelliJ IDEA Community Edition"
                                            >
                                            </textarea>
                                        </td>
                                        <td>
                                        <button
                                            type="button"
                                            class="remove-vi-row"
                                            onclick="removeVIRow(this)"
                                        >
                                            x
                                        </button>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td><input type="text" class="vi-num" value="3"></td>
                                        <td><input type="text" class="vi-type" placeholder="Самостоятельная работа"></td>
                                        <td><input type="text" class="vi-audience" placeholder=""></td>
                                        <td><textarea class="vi-equipment" rows="2" placeholder=""></textarea></td>
                                        <td><button type="button" class="remove-vi-row" onclick="removeVIRow(this)">×</button></td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                        <button type="button" class="add-vi-row-btn" onclick="addVIRow()">+ Добавить строку</button>
                    </div>
                `;
            } else if (item.id === 'VII') {
                editItem.innerHTML = `
                    <div class="edit-item-header">
                        <h3>VII. МЕТОДИЧЕСКИЕ УКАЗАНИЯ ДЛЯ ОБУЧАЮЩИХСЯ ПО ОСВОЕНИЮ ДИСЦИПЛИНЫ</h3>
                        <span class="edit-page">Стр. ${item.page}</span>
                    </div>
                    <div class="edit-item-content">
                        <label>Текст раздела:</label>
                        <textarea id="vii_content" class="edit-textarea" rows="10" placeholder="Введите методические указания для студентов..."></textarea>
                    </div>
                `;
            } else if (item.id === 'VIII') {
                editItem.innerHTML = `
                    <div class="edit-item-header">
                        <h3>VIII. ФОНД ОЦЕНОЧНЫХ СРЕДСТВ</h3>
                        <span class="edit-page">Стр. ${item.page}</span>
                    </div>
                    <div class="edit-item-content">
                        <label>8.1. Паспорт фонда оценочных средств</label>
                        <div id="table-viii-container" style="overflow-x: auto;">
                            <table class="table-viii-editor">
                                <thead>
                                    <tr>
                                        <th style="width: 60px;">№ п/п</th>
                                        <th style="min-width: 200px;">Код индикатора достижения компетенции</th>
                                        <th style="min-width: 300px;">Наименование оценочного средства</th>
                                        <th style="width: 40px;"></th>
                                    </tr>
                                </thead>
                                <tbody id="table-viii-body">
                                    <tr>
                                        <td>
                                            <input
                                                type="text"
                                                class="viii-num"
                                                value="1"
                                            >
                                        </td>
                                        <td>
                                            <input
                                                type="text"
                                                class="viii-code"
                                                placeholder="ОПК-1.1"
                                                value="ОПК-1.1"
                                            >
                                        </td>
                                        <td>
                                            <input
                                                type="text"
                                                class="viii-name"
                                                placeholder="Наименование оценочного средства"
                                                value="– лабораторные работы №№1-13 (тестирование)"
                                            >
                                        </td>
                                        <td>
                                            <button
                                                type="button"
                                                class="remove-viii-row"
                                                onclick="removeVIIIRow(this)"
                                            >
                                                x
                                            </button>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                        <button type="button" class="add-viii-row-btn" onclick="addVIIIRow()">+ Добавить строку</button>
                    </div>
                `;
            } else if (item.id === 'VIII') {
                editItem.innerHTML = `
                    <div class="edit-item-header">
                        <h3>VIII. ФОНД ОЦЕНОЧНЫХ СРЕДСТВ</h3>
                        <span class="edit-page">Стр. ${item.page}</span>
                    </div>
                    <div class="edit-item-content">
                        <label>8.1. Паспорт фонда оценочных средств</label>
                        <div id="table-viii-container" style="overflow-x: auto;">
                            <table class="table-viii-editor">
                                <thead>
                                    <tr>
                                        <th>№ п/п</th>
                                        <th>Код индикатора</th>
                                        <th>Наименование оценочного средства</th>
                                        <th></th>
                                    </tr>
                                </thead>
                                <tbody id="table-viii-body">
                                    <tr>
                                        <td>
                                            <input
                                                type="text"
                                                class="viii-num"
                                                value="1"
                                                style="width:50px"
                                            >
                                        </td>
                                        <td>
                                            <input
                                                type="text"
                                                class="viii-code"
                                                value="ОПК-1.1"
                                                style="width:200px"
                                            >
                                        </td>
                                        <td>
                                            <input
                                                type="text"
                                                class="viii-name"
                                                value="– лабораторные работы №№1-13 (тестирование)"
                                                style="width:300px"
                                            >
                                        </td>
                                        <td>
                                            <button
                                                type="button"
                                                class="remove-viii-row"
                                                onclick="removeVIIIRow(this)"
                                            >
                                                x
                                            </button>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                        <button type="button" class="add-viii-row-btn" onclick="addVIIIRow()">+ Добавить строку</button>

                        <label style="margin-top: 30px;">8.2. Лабораторные работы</label>
                        <div id="labs-container">
                            <div class="lab-item">
                                <div class="lab-header">
                                    <h4>Лабораторная работа №1</h4>
                                    <button type="button" class="remove-lab-btn" onclick="removeLab(this)">×</button>
                                </div>
                                <div class="lab-content">
                                    <label>Цель работы:</label>
                                    <textarea class="lab-goal" rows="2" placeholder="Введите цель..."></textarea>
                                    <label>Задачи:</label>
                                    <textarea class="lab-tasks" rows="2" placeholder="Введите задачи..."></textarea>
                                    <label>Теоретические сведения:</label>
                                    <textarea class="lab-theory" rows="3" placeholder="Введите теорию..."></textarea>
                                    <label>Порядок выполнения:</label>
                                    <textarea class="lab-steps" rows="3" placeholder="1. ..."></textarea>
                                    <label>Контрольные вопросы:</label>
                                    <textarea class="lab-questions" rows="2" placeholder="1. ..."></textarea>
                                </div>
                            </div>
                        </div>
                        <button type="button" class="add-lab-btn" onclick="addLab()">+ Добавить лабораторную работу</button>
                    </div>
                `;
            } else if (item.id === 'IX') {
                editItem.innerHTML = `
                    <div class="edit-item-header">
                        <h3>IX. ЗАКЛЮЧИТЕЛЬНЫЕ ПОЛОЖЕНИЯ</h3>
                        <span class="edit-page">Стр. ${item.page}</span>
                    </div>
                    <div class="edit-item-content">
                        <label>Текст заключительных положений:</label>
                        <textarea
                            id="ix_text"
                            class="edit-textarea"
                            rows="4"
                            placeholder="Пример:&#10;Зачёт по дисциплине выставляется, если студент набрал 60 и более баллов."
                        >
                        </textarea>
                    </div>
                `;
            }
            container.appendChild(editItem);
            if (item.id === 'I' || item.id === 'II') {
                const textarea = document.getElementById(`content_${index}`);
                if (textarea) {
                    textarea.addEventListener('input', function(e) {
                        currentTocItems[index].content = e.target.value;
                    });
                }
            }
        }
    });

    if (container.children.length === 0) {
        container.innerHTML = '<div class="empty-toc">Нет доступных разделов для редактирования</div>';
    }
}

function addCompetence() {
    const container = document.getElementById('competencies-container');
    const newComp = document.createElement('div');
    newComp.className = 'competence-item';
    newComp.innerHTML = `
        <input type="text" class="competence-field" placeholder="Компетенция" value="">
        <input type="text" class="indicator-field" placeholder="Индикатор" value="">
        <textarea class="results-field" rows="4" placeholder="Результаты обучения..."></textarea>
        <button type="button" class="remove-competence-btn" onclick="removeCompetence(this)">×</button>
    `;
    container.appendChild(newComp);
}

function removeCompetence(btn) {
    if (confirm('Удалить эту компетенцию?')) {
        btn.parentElement.remove();
    }
}

function addVIRow() {
    const tbody = document.getElementById('table-vi-body');
    const newRow = document.createElement('tr');
    const rowCount = tbody.children.length + 1;

    newRow.innerHTML = `
        <td><input type="text" class="vi-num" value="${rowCount}"></td>
        <td><input type="text" class="vi-type" placeholder="Тип аудиторного занятия"></td>
        <td><input type="text" class="vi-audience" placeholder="Рекомендуемая аудитория"></td>
        <td><textarea class="vi-equipment" rows="2" placeholder="Оснащение..."></textarea></td>
        <td><button type="button" class="remove-vi-row" onclick="removeVIRow(this)">×</button></td>
    `;
    tbody.appendChild(newRow);
}

function removeVIRow(btn) {
    const tbody = document.getElementById('table-vi-body');
    if (tbody.children.length > 1) {
        btn.closest('tr').remove();
        const rows = tbody.children;
        for (let i = 0; i < rows.length; i++) {
            rows[i].cells[0].querySelector('input').value = i + 1;
        }
    } else {
        alert('Должна быть хотя бы одна строка');
    }
}

function collectTableVIData() {
    const rows = [];
    const tableRows = document.querySelectorAll('#table-vi-body tr');
    tableRows.forEach(row => {
        rows.push({
            num: row.querySelector('.vi-num')?.value || '',
            type: row.querySelector('.vi-type')?.value || '',
            audience: row.querySelector('.vi-audience')?.value || '',
            equipment: row.querySelector('.vi-equipment')?.value || ''
        });
    });
    return rows;
}

function addVIIIRow() {
    const tbody = document.getElementById('table-viii-body');
    const newRow = document.createElement('tr');
    const rowCount = tbody.children.length + 1;

    newRow.innerHTML = `
        <td><input type="text" class="viii-num" value="${rowCount}"></td>
        <td><input type="text" class="viii-code" placeholder="Код индикатора"></td>
        <td><input type="text" class="viii-name" placeholder="Наименование оценочного средства"></td>
        <td><button type="button" class="remove-viii-row" onclick="removeVIIIRow(this)">×</button></td>
    `;
    tbody.appendChild(newRow);
}

function removeVIIIRow(btn) {
    const tbody = document.getElementById('table-viii-body');
    if (tbody.children.length > 1) {
        btn.closest('tr').remove();
        const rows = tbody.children;
        for (let i = 0; i < rows.length; i++) {
            rows[i].cells[0].querySelector('input').value = i + 1;
        }
    } else {
        alert('Должна быть хотя бы одна строка');
    }
}

function collectTableVIIIData() {
    const rows = [];
    const tableRows = document.querySelectorAll('#table-viii-body tr');
    tableRows.forEach(row => {
        rows.push({
            num: row.querySelector('.viii-num')?.value || '',
            code: row.querySelector('.viii-code')?.value || '',
            name: row.querySelector('.viii-name')?.value || ''
        });
    });
    return rows;
}

let labCounter = 1;

function addLab() {
    const container = document.getElementById('labs-container');
    labCounter++;
    const newLab = document.createElement('div');
    newLab.className = 'lab-item';
    newLab.setAttribute('data-lab', labCounter);
    newLab.innerHTML = `
        <div class="lab-header">
            <h4>Лабораторная работа №${labCounter}</h4>
            <button type="button" class="remove-lab-btn" onclick="removeLab(this)">×</button>
        </div>
        <div class="lab-content">
            <label>Цель работы:</label>
            <textarea class="lab-goal" rows="2" placeholder="Введите цель лабораторной работы..."></textarea>

            <label>Задачи:</label>
            <textarea class="lab-tasks" rows="3" placeholder="Введите задачи..."></textarea>

            <label>Теоретические сведения:</label>
            <textarea class="lab-theory" rows="4" placeholder="Введите теоретические сведения..."></textarea>

            <label>Порядок выполнения:</label>
            <textarea class="lab-steps" rows="4" placeholder="1. ...\n2. ...\n3. ..."></textarea>

            <label>Контрольные вопросы:</label>
            <textarea class="lab-questions" rows="3" placeholder="1. ...\n2. ..."></textarea>
        </div>
    `;
    container.appendChild(newLab);
}

function removeLab(btn) {
    if (confirm('Удалить эту лабораторную работу?')) {
        btn.closest('.lab-item').remove();
    }
}

function collectLabsData() {
    const labs = [];
    document.querySelectorAll('#labs-container .lab-item').forEach((item, idx) => {
        labs.push({
            number: idx + 1,
            goal: item.querySelector('.lab-goal')?.value || '',
            tasks: item.querySelector('.lab-tasks')?.value || '',
            theory: item.querySelector('.lab-theory')?.value || '',
            steps: item.querySelector('.lab-steps')?.value || '',
            questions: item.querySelector('.lab-questions')?.value || ''
        });
    });
    return labs;
}

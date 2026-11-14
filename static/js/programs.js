// Страница «Сохранённые программы»: загружает список с сервера и рисует таблицу.

const statusLine = document.getElementById('programs-status');
const table = document.getElementById('programs-table');
const tableBody = document.getElementById('programs-body');

const dateFormat = new Intl.DateTimeFormat('ru-RU', { dateStyle: 'medium', timeStyle: 'short' });

function showStatus(text) {
    statusLine.textContent = text;
    statusLine.hidden = false;
    table.hidden = true;
}

// Ячейки создаются через textContent, а не innerHTML: так текст из базы
// никогда не будет выполнен как HTML-код.
function addCell(row, text, className) {
    const cell = row.insertCell();
    cell.textContent = text;
    if (className) cell.className = className;
    return cell;
}

function renderPrograms(programs) {
    tableBody.replaceChildren();

    if (programs.length === 0) {
        showStatus('Пока нет сохранённых программ. Создайте первую — она появится здесь.');
        return;
    }

    for (const program of programs) {
        const row = tableBody.insertRow();
        addCell(row, program.discipline_name, 'discipline');
        addCell(row, program.teacher_name || '—');
        addCell(row, dateFormat.format(new Date(program.updated_at)));

        const actions = addCell(row, '', 'actions');

        const download = document.createElement('a');
        download.href = `/api/programs/${program.id}/docx`;
        download.textContent = 'Скачать .docx';
        download.className = 'action-download';
        actions.append(download);

        const remove = document.createElement('button');
        remove.type = 'button';
        remove.textContent = 'Удалить';
        remove.className = 'action-delete';
        remove.addEventListener('click', () => deleteProgram(program));
        actions.append(remove);
    }

    statusLine.hidden = true;
    table.hidden = false;
}

async function loadPrograms() {
    try {
        const response = await fetch('/api/programs');
        if (!response.ok) throw new Error('Ошибка сервера: ' + response.status);
        renderPrograms(await response.json());
    } catch (error) {
        console.error(error);
        showStatus('Не удалось загрузить список программ. Обновите страницу.');
    }
}

async function deleteProgram(program) {
    if (!confirm(`Удалить программу «${program.discipline_name}»? Вернуть её будет нельзя.`)) return;

    try {
        const response = await fetch(`/api/programs/${program.id}`, { method: 'DELETE' });
        if (!response.ok) throw new Error('Ошибка сервера: ' + response.status);
        await loadPrograms();
    } catch (error) {
        console.error(error);
        alert('Не удалось удалить программу: ' + error.message);
    }
}

loadPrograms();

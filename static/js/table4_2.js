function addTable42Row() {
    const tbody = document.getElementById('table-42-body');
    const newRow = document.createElement('tr');
    const rowCount = tbody.children.length + 1;

    newRow.innerHTML = `
        <td><input type="text" class="table-input" value="${rowCount}"></td>
        <td><input type="text" class="table-input" placeholder="Тема занятия"></td>
        <td><input type="text" class="table-input" value="1"></td>
        <td><input type="text" class="table-input" value="${rowCount}"></td>
        <td><textarea class="table-textarea" rows="2" placeholder="Вид самостоятельной работы..."></textarea></td>
        <td><input type="text" class="table-input" value="8"></td>
        <td><input type="text" class="table-input" value="-"></td>
        <td><button type="button" class="remove-row-btn" onclick="removeTable42Row(this)">×</button></td>
    `;
    tbody.appendChild(newRow);
}

function removeTable42Row(btn) {
    const tbody = document.getElementById('table-42-body');
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

function collectTable42Data() {
    const rows = [];
    const tableRows = document.querySelectorAll('#table-42-body tr');
    tableRows.forEach(row => {
        const inputs = row.querySelectorAll('input');
        const textarea = row.querySelector('textarea');
        rows.push({
            num: inputs[0]?.value || '',
            topic: inputs[1]?.value || '',
            semester: inputs[2]?.value || '',
            deadline: inputs[3]?.value || '',
            work_type: textarea?.value || '',
            hours: inputs[4]?.value || '',
            materials: inputs[5]?.value || ''
        });
    });
    return rows;
}

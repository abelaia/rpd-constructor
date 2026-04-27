function addTableRow() {
    const tbody = document.getElementById('table-41-body');
    const newRow = document.createElement('tr');
    const rowCount = tbody.children.length + 1;

    newRow.innerHTML = `
        <td><input type="text" class="table-input" value="${rowCount}"></td>
        <td><input type="text" class="table-input" placeholder="Название темы"></td>
        <td><input type="text" class="table-input" value="-"></td>
        <td><input type="text" class="table-input" value="-"></td>
        <td><input type="text" class="table-input" value="-"></td>
        <td><input type="text" class="table-input" value="-"></td>
        <td><input type="text" class="table-input" value="-"></td>
        <td><input type="text" class="table-input" value="-"></td>
        <td><input type="text" class="table-input" value="-"></td>
        <td><input type="text" class="table-input" value="-"></td>
        <td><input type="text" class="table-input" value="-"></td>
        <td><button type="button" class="remove-row-btn" onclick="removeTableRow(this)">×</button></td>
    `;
    tbody.appendChild(newRow);
}

function removeTableRow(btn) {
    const tbody = document.getElementById('table-41-body');
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

function collectTable41Data() {
    const rows = [];
    const tableRows = document.querySelectorAll('#table-41-body tr');
    tableRows.forEach(row => {
        const inputs = row.querySelectorAll('input');
        rows.push({
            num: inputs[0]?.value || '',
            topic: inputs[1]?.value || '',
            lectures: inputs[2]?.value || '',
            practical: inputs[3]?.value || '',
            laboratory: inputs[4]?.value || '',
            consultations: inputs[5]?.value || '',
            independent: inputs[6]?.value || '',
            format: inputs[7]?.value || '',
            assessment: inputs[8]?.value || '',
            control_type: inputs[9]?.value || '',
            points: inputs[10]?.value || ''
        });
    });
    return rows;
}

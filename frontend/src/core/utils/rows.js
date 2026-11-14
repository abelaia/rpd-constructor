/**
 * @template {{id: string}} Row
 * @param {Row[]} rows
 * @param {string} id
 * @param {string} key
 * @param {string} value
 * @returns {Row[]}
 */
export function updateRow(rows, id, key, value) {
    return rows.map((row) => (row.id === id ? {...row, [key]: value} : row));
}

/**
 * @template {{id: string}} Row
 * @param {Row[]} rows
 * @param {string} id
 * @returns {Row[]}
 */
export function removeRow(rows, id) {
    return rows.filter((row) => row.id !== id);
}

/**
 * @template Row
 * @param {Row[]} rows
 * @param {number} fromIndex
 * @param {number} toIndex
 * @returns {Row[]}
 */
export function moveRow(rows, fromIndex, toIndex) {
    const isOutOfRange = [fromIndex, toIndex].some((index) => index < 0 || index >= rows.length);

    if (isOutOfRange || fromIndex === toIndex) {
        return rows;
    }

    const nextRows = [...rows];
    const [movedRow] = nextRows.splice(fromIndex, 1);
    nextRows.splice(toIndex, 0, movedRow);

    return nextRows;
}

/**
 * @param {string} id
 * @param {readonly string[]} keys
 * @returns {Record<string, string> & {id: string}}
 */
export function createRow(id, keys) {
    return {id, ...Object.fromEntries(keys.map((key) => [key, '']))};
}

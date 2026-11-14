const LIST_MARKER = /^[-–—•]\s*/;

/**
 * @typedef {object} PreviewLine
 * @property {string} id
 * @property {string} text
 * @property {boolean} isListItem
 */

/**
 * @param {string} text
 * @returns {PreviewLine[]}
 */
export function getPreviewLines(text) {
    return text
        .split('\n')
        .map((line) => line.trim())
        .filter(Boolean)
        .map((line, index) => ({
            id: `${index}-${line}`,
            text: line.replace(LIST_MARKER, ''),
            isListItem: LIST_MARKER.test(line),
        }));
}

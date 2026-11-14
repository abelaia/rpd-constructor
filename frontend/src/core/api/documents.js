import {request} from '@/core/api/client';

const GENERATE_WORD_PATH = '/generate-word';
const FALLBACK_FILENAME = 'rpd.docx';
const FILENAME_PATTERN = /filename="?([^";]+)"?/i;

/**
 * @param {string | null} contentDisposition
 * @returns {string}
 */
export function getFilename(contentDisposition) {
    return contentDisposition?.match(FILENAME_PATTERN)?.[1] ?? FALLBACK_FILENAME;
}

/**
 * @param {object} generateRequest результат toGenerateRequest
 * @returns {Promise<{blob: Blob, filename: string}>}
 */
export async function generateWord(generateRequest) {
    const response = await request(GENERATE_WORD_PATH, {method: 'POST', body: JSON.stringify(generateRequest)});
    const blob = await response.blob();

    return {blob, filename: getFilename(response.headers.get('Content-Disposition'))};
}

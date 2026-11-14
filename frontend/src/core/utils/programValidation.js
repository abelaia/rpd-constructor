import {PROGRAM_NAME_MAX_LENGTH, START_MODES} from '@/core/constants';

/**
 * @param {string} name
 * @returns {string | null} текст ошибки или null
 */
export function validateProgramName(name) {
    const trimmedName = name.trim();

    if (trimmedName === '') {
        return 'Введите название дисциплины';
    }

    if (trimmedName.length > PROGRAM_NAME_MAX_LENGTH) {
        return `Название длиннее ${PROGRAM_NAME_MAX_LENGTH} символов`;
    }

    return null;
}

/**
 * @param {string} mode значение из START_MODES
 * @param {string} sourceId
 * @returns {string | null} текст ошибки или null
 */
export function validateSource(mode, sourceId) {
    return mode === START_MODES.copy && sourceId === '' ? 'Выберите программу, с которой сделать копию' : null;
}

import {ApiError} from '@/core/api/client';

const NETWORK_ERROR_MESSAGE = 'Нет связи с сервером. Проверьте, что он запущен, и попробуйте ещё раз';
const SERVER_ERROR_MESSAGE = 'Не удалось собрать документ. Проверьте заполнение разделов и попробуйте ещё раз';
const FALLBACK_MESSAGE = 'Что-то пошло не так, попробуйте ещё раз';

/**
 * @param {unknown} error
 * @returns {string}
 */
export function getErrorMessage(error) {
    if (!(error instanceof ApiError)) {
        return FALLBACK_MESSAGE;
    }

    return error.status === 0 ? NETWORK_ERROR_MESSAGE : SERVER_ERROR_MESSAGE;
}

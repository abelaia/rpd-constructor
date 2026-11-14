const MORNING_START_HOUR = 5;
const DAY_START_HOUR = 12;
const EVENING_START_HOUR = 18;

const CHANGED_AT_FORMAT = new Intl.DateTimeFormat('ru-RU', {
    day: 'numeric',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit',
});

const TIME_FORMAT = new Intl.DateTimeFormat('ru-RU', {hour: '2-digit', minute: '2-digit'});

/**
 * @param {string} isoDate
 * @returns {string} например «14 нояб., 14:58»
 */
export function formatChangedAt(isoDate) {
    return CHANGED_AT_FORMAT.format(new Date(isoDate));
}

/**
 * @param {string} isoDate
 * @returns {string} например «14:58»
 */
export function formatTime(isoDate) {
    return TIME_FORMAT.format(new Date(isoDate));
}

/**
 * @param {number} hour час от 0 до 23
 * @returns {string}
 */
export function getGreeting(hour) {
    if (hour >= MORNING_START_HOUR && hour < DAY_START_HOUR) {
        return 'Доброе утро';
    }

    if (hour >= DAY_START_HOUR && hour < EVENING_START_HOUR) {
        return 'Добрый день';
    }

    return 'Добрый вечер';
}

/**
 * @param {number} count
 * @param {[string, string, string]} forms формы для 1, 2 и 5: ['раздел', 'раздела', 'разделов']
 * @returns {string}
 */
export function pluralize(count, forms) {
    const lastTwoDigits = Math.abs(count) % 100;
    const lastDigit = lastTwoDigits % 10;

    if (lastTwoDigits > 10 && lastTwoDigits < 20) {
        return forms[2];
    }

    if (lastDigit === 1) {
        return forms[0];
    }

    if (lastDigit >= 2 && lastDigit <= 4) {
        return forms[1];
    }

    return forms[2];
}

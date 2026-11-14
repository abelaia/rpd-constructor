const RANDOM_RADIX = 36;
const RANDOM_START = 2;

/** @returns {string} */
export function createId() {
    if (typeof crypto !== 'undefined' && typeof crypto.randomUUID === 'function') {
        return crypto.randomUUID();
    }

    return `${Date.now().toString(RANDOM_RADIX)}-${Math.random().toString(RANDOM_RADIX).slice(RANDOM_START)}`;
}

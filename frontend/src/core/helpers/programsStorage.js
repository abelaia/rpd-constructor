import {safeStorage} from '@/core/helpers/safeStorage';
import {createEmptySections} from '@/core/utils/programs';

/** @typedef {import('@/core/types/program').Program} Program */

const STORAGE_KEY = 'rpd.programs';

/**
 * @param {Program} program
 * @returns {Program}
 */
function withAllSections(program) {
    return {...program, sections: {...createEmptySections(), ...program.sections}};
}

/** @returns {Program[]} */
export function loadPrograms() {
    const stored = safeStorage.get(STORAGE_KEY);

    if (!stored) {
        return [];
    }

    try {
        const programs = JSON.parse(stored);

        return Array.isArray(programs) ? programs.map(withAllSections) : [];
    } catch (error) {
        console.error(error);

        return [];
    }
}

/** @param {Program[]} programs */
export function savePrograms(programs) {
    safeStorage.set(STORAGE_KEY, JSON.stringify(programs));
}

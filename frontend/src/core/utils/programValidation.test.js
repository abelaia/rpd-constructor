import {describe, expect, it} from 'vitest';
import {PROGRAM_NAME_MAX_LENGTH, START_MODES} from '@/core/constants';
import {validateProgramName, validateSource} from '@/core/utils/programValidation';

describe('programValidation', () => {
    it('не пропускает пустое название и название из пробелов', () => {
        expect(validateProgramName('')).not.toBeNull();
        expect(validateProgramName('   ')).not.toBeNull();
    });

    it('не пропускает слишком длинное название', () => {
        expect(validateProgramName('а'.repeat(PROGRAM_NAME_MAX_LENGTH + 1))).not.toBeNull();
    });

    it('пропускает обычное название', () => {
        expect(validateProgramName('Базы данных')).toBeNull();
    });

    it('требует исходную программу только для копии', () => {
        expect(validateSource(START_MODES.copy, '')).not.toBeNull();
        expect(validateSource(START_MODES.copy, 'program')).toBeNull();
        expect(validateSource(START_MODES.blank, '')).toBeNull();
    });
});

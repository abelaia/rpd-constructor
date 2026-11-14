import {describe, expect, it} from 'vitest';
import {CHECK_LEVELS, SECTION_STATUS} from '@/core/constants';
import {SECTIONS} from '@/core/data/sections';
import {
    createProgram,
    getChecks,
    getDoneCount,
    getHoursTotals,
    getPointsTotal,
    getSectionStatus,
    toGenerateRequest,
    toNumber,
} from '@/core/utils/programs';

const NOW = '2026-11-14T11:58:00.000Z';

function getSection(id) {
    return SECTIONS.find((section) => section.id === id);
}

function createTopic(overrides) {
    return {
        id: 'topic',
        topic: 'Тема',
        lectures: '',
        practical: '',
        laboratory: '',
        consultations: '',
        independent: '',
        format: '',
        assessment: '',
        points: '',
        ...overrides,
    };
}

function createFilledProgram() {
    const program = createProgram({id: 'program', name: 'Базы данных', now: NOW});

    return {
        ...program,
        totalHours: '72',
        sections: {
            ...program.sections,
            topics: [
                createTopic({id: 'first', lectures: '18', practical: '8', independent: '10', points: '40'}),
                createTopic({id: 'second', laboratory: '16', consultations: '2', independent: '18', points: '60'}),
            ],
        },
    };
}

describe('programs', () => {
    it('превращает строку с запятой в число, а мусор — в ноль', () => {
        expect(toNumber('2,5')).toBe(2.5);
        expect(toNumber('abc')).toBe(0);
        expect(toNumber('')).toBe(0);
    });

    it('считает часы по видам занятий и общий итог', () => {
        const totals = getHoursTotals(createFilledProgram().sections.topics);

        expect(totals).toEqual({
            lectures: 18,
            practical: 8,
            laboratory: 16,
            consultations: 2,
            independent: 28,
            total: 72,
        });
    });

    it('считает сумму баллов по темам', () => {
        expect(getPointsTotal(createFilledProgram().sections.topics)).toBe(100);
    });

    it('считает раздел IV заполненным, когда часы и баллы сходятся', () => {
        expect(getSectionStatus(createFilledProgram(), getSection('IV'))).toBe(SECTION_STATUS.done);
    });

    it('помечает раздел IV ошибкой, когда баллов больше ста', () => {
        const program = createFilledProgram();
        const topics = [...program.sections.topics, createTopic({id: 'third', points: '5'})];

        expect(getSectionStatus({...program, sections: {...program.sections, topics}}, getSection('IV'))).toBe(
            SECTION_STATUS.error,
        );
    });

    it('у новой программы титул в работе, а разделы пусты', () => {
        const program = createProgram({id: 'program', name: 'Базы данных', now: NOW});

        expect(getSectionStatus(program, getSection('title'))).toBe(SECTION_STATUS.inProgress);
        expect(getSectionStatus(program, getSection('I'))).toBe(SECTION_STATUS.empty);
        expect(getDoneCount(program)).toBe(0);
    });

    it('сообщает о пустой литературе и сошедшихся суммах', () => {
        const levels = Object.fromEntries(getChecks(createFilledProgram()).map((check) => [check.id, check.level]));

        expect(levels).toEqual({
            points: CHECK_LEVELS.ok,
            hours: CHECK_LEVELS.ok,
            literature: CHECK_LEVELS.error,
        });
    });

    it('собирает запрос в формате backend: номера строк, целые часы, без внутренних id', () => {
        const request = toGenerateRequest({...createFilledProgram(), disciplineNameEn: 'Databases'});

        expect(request.discipline_name).toBe('Databases (Базы данных)');
        expect(request.total_hours).toBe(72);
        expect(request.toc_items).toHaveLength(9);
        expect(request.section_contents.IV_table[1]).toMatchObject({num: '2', laboratory: '16', control_type: ''});
        expect(request.section_contents.IV_table[0]).not.toHaveProperty('id');
    });

    it('не отправляет пустые вводные тексты, чтобы backend подставил свои', () => {
        const {section_contents: sectionContents} = toGenerateRequest(createFilledProgram());

        expect(sectionContents.III_desc).toBeUndefined();
        expect(sectionContents.VI_description).toBeUndefined();
    });
});

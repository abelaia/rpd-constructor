import {
    CHECK_LEVELS,
    DEFAULT_ATTESTATION_FORM,
    DEFAULT_CREDITS,
    DEFAULT_TOTAL_HOURS,
    MAX_POINTS,
    SECTION_KINDS,
    SECTION_STATUS,
} from '@/core/constants';
import {CONTENT_SECTIONS, SECTIONS} from '@/core/data/sections';

/** @typedef {import('@/core/types/program').Program} Program */
/** @typedef {import('@/core/types/program').ProgramSections} ProgramSections */
/** @typedef {import('@/core/types/program').ProgramCheck} ProgramCheck */
/** @typedef {import('@/core/types/program').SectionInfo} SectionInfo */
/** @typedef {import('@/core/types/program').TopicRow} TopicRow */

const HOUR_KEYS = Object.freeze(['lectures', 'practical', 'laboratory', 'consultations', 'independent']);
const TITLE_REQUIRED_FIELDS = Object.freeze([
    'disciplineName',
    'teacherName',
    'teacherTitle',
    'department',
    'umsDate',
    'umsProtocol',
]);
const COMPETENCY_REQUIRED_FIELDS = Object.freeze(['competence', 'indicator', 'knowledge', 'skills', 'abilities']);
const LAB_REQUIRED_FIELDS = Object.freeze(['goal', 'tasks', 'steps']);
const EQUIPMENT_REQUIRED_FIELDS = Object.freeze(['type', 'equipment']);

/**
 * @param {unknown} value
 * @returns {number}
 */
export function toNumber(value) {
    const number = Number.parseFloat(String(value ?? '').replace(',', '.'));

    return Number.isFinite(number) ? number : 0;
}

/**
 * @param {unknown} value
 * @returns {boolean}
 */
function hasText(value) {
    return String(value ?? '').trim().length > 0;
}

/** @returns {ProgramSections} */
export function createEmptySections() {
    return {
        goals: '',
        position: '',
        competenciesIntro: '',
        competencies: [],
        topics: [],
        selfStudy: [],
        mainLiterature: '',
        additionalLiterature: '',
        internetResources: '',
        equipmentIntro: '',
        equipment: [],
        guidelines: '',
        assessmentCodes: [],
        labs: [],
        finalProvisions: '',
    };
}

/**
 * @param {{id: string, name: string, now: string}} options
 * @returns {Program}
 */
export function createProgram({id, name, now}) {
    return {
        id,
        createdAt: now,
        changedAt: now,
        disciplineName: name.trim(),
        disciplineNameEn: '',
        code: '',
        semester: '',
        teacherName: '',
        teacherTitle: '',
        department: '',
        umsDate: '',
        umsProtocol: '',
        credits: DEFAULT_CREDITS,
        totalHours: DEFAULT_TOTAL_HOURS,
        attestationForm: DEFAULT_ATTESTATION_FORM,
        sections: createEmptySections(),
    };
}

/**
 * @param {TopicRow[]} rows
 * @returns {{lectures: number, practical: number, laboratory: number, consultations: number, independent: number, total: number}}
 */
export function getHoursTotals(rows) {
    const totals = Object.fromEntries(
        HOUR_KEYS.map((key) => [key, rows.reduce((sum, row) => sum + toNumber(row[key]), 0)]),
    );

    return {...totals, total: HOUR_KEYS.reduce((sum, key) => sum + totals[key], 0)};
}

/**
 * @param {TopicRow[]} rows
 * @returns {number}
 */
export function getPointsTotal(rows) {
    return rows.reduce((sum, row) => sum + toNumber(row.points), 0);
}

/**
 * @param {object[]} items
 * @param {readonly string[]} requiredFields
 * @returns {string}
 */
function getListStatus(items, requiredFields) {
    if (items.length === 0) {
        return SECTION_STATUS.empty;
    }

    const isComplete = items.every((item) => requiredFields.every((field) => hasText(item[field])));

    return isComplete ? SECTION_STATUS.done : SECTION_STATUS.inProgress;
}

/**
 * @param {Program} program
 * @returns {string}
 */
function getTitleStatus(program) {
    const filledCount = TITLE_REQUIRED_FIELDS.filter((field) => hasText(program[field])).length;

    if (filledCount === 0) {
        return SECTION_STATUS.empty;
    }

    return filledCount === TITLE_REQUIRED_FIELDS.length ? SECTION_STATUS.done : SECTION_STATUS.inProgress;
}

/**
 * @param {Program} program
 * @returns {string}
 */
function getContentStatus(program) {
    const {topics} = program.sections;

    if (topics.length === 0) {
        return SECTION_STATUS.empty;
    }

    const hours = getHoursTotals(topics).total;
    const points = getPointsTotal(topics);
    const plannedHours = toNumber(program.totalHours);

    if (hours > plannedHours || points > MAX_POINTS) {
        return SECTION_STATUS.error;
    }

    return hours === plannedHours && points === MAX_POINTS ? SECTION_STATUS.done : SECTION_STATUS.inProgress;
}

/**
 * @param {Program} program
 * @returns {string}
 */
function getLiteratureStatus(program) {
    const {mainLiterature, additionalLiterature, internetResources} = program.sections;

    if (hasText(mainLiterature)) {
        return SECTION_STATUS.done;
    }

    return hasText(additionalLiterature) || hasText(internetResources)
        ? SECTION_STATUS.inProgress
        : SECTION_STATUS.empty;
}

/**
 * @param {Program} program
 * @param {SectionInfo} section
 * @returns {string} значение из SECTION_STATUS
 */
export function getSectionStatus(program, section) {
    const {sections} = program;

    if (section.kind === SECTION_KINDS.title) {
        return getTitleStatus(program);
    }

    if (section.kind === SECTION_KINDS.text) {
        return hasText(sections[section.field]) ? SECTION_STATUS.done : SECTION_STATUS.empty;
    }

    if (section.kind === SECTION_KINDS.competencies) {
        return getListStatus(sections.competencies, COMPETENCY_REQUIRED_FIELDS);
    }

    if (section.kind === SECTION_KINDS.content) {
        return getContentStatus(program);
    }

    if (section.kind === SECTION_KINDS.literature) {
        return getLiteratureStatus(program);
    }

    if (section.kind === SECTION_KINDS.equipment) {
        return getListStatus(sections.equipment, EQUIPMENT_REQUIRED_FIELDS);
    }

    return getListStatus(sections.labs, LAB_REQUIRED_FIELDS);
}

/**
 * @param {Program} program
 * @returns {Record<string, string>} статус по id раздела
 */
export function getSectionStatuses(program) {
    return Object.fromEntries(SECTIONS.map((section) => [section.id, getSectionStatus(program, section)]));
}

/**
 * @param {Program} program
 * @returns {number} сколько разделов I–IX заполнено
 */
export function getDoneCount(program) {
    return CONTENT_SECTIONS.filter((section) => getSectionStatus(program, section) === SECTION_STATUS.done).length;
}

/**
 * @param {Program} program
 * @returns {boolean}
 */
export function isProgramDone(program) {
    return getDoneCount(program) === CONTENT_SECTIONS.length;
}

/**
 * @param {number} value
 * @param {number} target
 * @returns {string} значение из CHECK_LEVELS
 */
function getSumLevel(value, target) {
    if (value === target) {
        return CHECK_LEVELS.ok;
    }

    return value > target ? CHECK_LEVELS.error : CHECK_LEVELS.warning;
}

/**
 * @param {Program} program
 * @returns {ProgramCheck[]}
 */
export function getChecks(program) {
    const {topics, mainLiterature} = program.sections;
    const points = getPointsTotal(topics);
    const hours = getHoursTotals(topics).total;
    const plannedHours = toNumber(program.totalHours);
    const pointsLevel = getSumLevel(points, MAX_POINTS);
    const hoursLevel = getSumLevel(hours, plannedHours);
    const hasLiterature = hasText(mainLiterature);

    return [
        {
            id: 'points',
            level: pointsLevel,
            title: `Сумма баллов ${points} из ${MAX_POINTS}`,
            hint:
                pointsLevel === CHECK_LEVELS.ok
                    ? 'Баллы распределены полностью'
                    : `Раздел IV: разница ${Math.abs(MAX_POINTS - points)}`,
            sectionId: 'IV',
        },
        {
            id: 'hours',
            level: hoursLevel,
            title: `Часы по плану ${hours} из ${plannedHours}`,
            hint:
                hoursLevel === CHECK_LEVELS.ok
                    ? 'Сходится с учебным планом'
                    : `Раздел IV: разница ${Math.abs(plannedHours - hours)}`,
            sectionId: 'IV',
        },
        {
            id: 'literature',
            level: hasLiterature ? CHECK_LEVELS.ok : CHECK_LEVELS.error,
            title: hasLiterature ? 'Литература указана' : 'Не указана литература',
            hint: hasLiterature ? 'Основной список заполнен' : 'Раздел V: основной список пуст',
            sectionId: 'V',
        },
    ];
}

/**
 * @param {import('@/core/types/program').Competency} competency
 * @returns {string}
 */
export function getCompetencyResults(competency) {
    return [
        ['Знать', competency.knowledge],
        ['Уметь', competency.skills],
        ['Владеть', competency.abilities],
    ]
        .filter(([, text]) => hasText(text))
        .map(([label, text]) => `${label}: ${text.trim()}`)
        .join('\n');
}

/**
 * @param {Program} program
 * @returns {string}
 */
export function getDocumentName(program) {
    const {disciplineName, disciplineNameEn} = program;

    return hasText(disciplineNameEn) ? `${disciplineNameEn.trim()} (${disciplineName.trim()})` : disciplineName.trim();
}

/**
 * @param {{id: string}} row
 * @returns {Record<string, unknown>}
 */
function omitId(row) {
    return Object.fromEntries(Object.entries(row).filter(([key]) => key !== 'id'));
}

/**
 * @template {{id: string}} Row
 * @param {Row[]} rows
 * @returns {Array<Omit<Row, 'id'> & {num: string}>}
 */
function toNumberedRows(rows) {
    return rows.map((row, index) => ({num: String(index + 1), ...omitId(row)}));
}

/**
 * Тело запроса POST /generate-word — зеркало RPDGenerateRequest в app/schemas.py.
 * @param {Program} program
 * @returns {object}
 */
export function toGenerateRequest(program) {
    const {sections} = program;
    const credits = Math.round(toNumber(program.credits));
    const totalHours = Math.round(toNumber(program.totalHours));

    return {
        discipline_name: getDocumentName(program),
        teacher_name: program.teacherName,
        teacher_title: program.teacherTitle,
        department: program.department,
        ums_date: program.umsDate,
        ums_protocol: program.umsProtocol,
        credits,
        total_hours: totalHours,
        attestation_form: program.attestationForm,
        custom_filename: null,
        toc_items: CONTENT_SECTIONS.map((section) => ({
            id: section.id,
            title: `${section.numeral}. ${section.documentTitle}`,
            page: '',
        })),
        toc_subitems: {},
        section_contents: {
            I: sections.goals,
            II: sections.position,
            III_desc: sections.competenciesIntro,
            III_competencies: sections.competencies.map((competency) => ({
                competence: competency.competence,
                indicator: competency.indicator,
                results: getCompetencyResults(competency),
            })),
            IV_credits: credits,
            IV_hours: totalHours,
            IV_attestation: program.attestationForm,
            IV_table: toNumberedRows(sections.topics).map((row) => ({...row, control_type: ''})),
            IV_table42: toNumberedRows(sections.selfStudy),
            V_main_literature: sections.mainLiterature,
            V_additional_literature: sections.additionalLiterature,
            V_internet_resources: sections.internetResources,
            VI_description: sections.equipmentIntro,
            VI_table: toNumberedRows(sections.equipment),
            VII: sections.guidelines,
            VIII_table: toNumberedRows(sections.assessmentCodes),
            VIII_labs: sections.labs.map((lab, index) => ({number: index + 1, ...omitId(lab)})),
            IX: sections.finalProvisions,
        },
    };
}

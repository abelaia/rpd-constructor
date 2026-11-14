export const ROUTE_NAMES = Object.freeze({
    programs: 'programs',
    editor: 'editor',
    ready: 'ready',
});

export const SECTION_KINDS = Object.freeze({
    title: 'title',
    text: 'text',
    competencies: 'competencies',
    content: 'content',
    literature: 'literature',
    equipment: 'equipment',
    assessment: 'assessment',
});

export const SECTION_STATUS = Object.freeze({
    empty: 'empty',
    inProgress: 'in-progress',
    done: 'done',
    error: 'error',
});

export const CHECK_LEVELS = Object.freeze({
    ok: 'ok',
    warning: 'warning',
    error: 'error',
});

export const PROGRAM_FILTERS = Object.freeze({
    all: 'all',
    inProgress: 'in-progress',
    done: 'done',
});

export const START_MODES = Object.freeze({
    blank: 'blank',
    copy: 'copy',
    template: 'template',
});

export const TITLE_SECTION_ID = 'title';
export const MAX_POINTS = 100;
export const DEFAULT_CREDITS = '2';
export const DEFAULT_TOTAL_HOURS = '72';
export const DEFAULT_ATTESTATION_FORM = 'зачёт';
export const PROGRAM_NAME_MAX_LENGTH = 160;

const HOURS_COLUMN_WIDTH = '56px';

/** @type {readonly import('@/core/types/program').TableColumn[]} */
export const TOPIC_COLUMNS = Object.freeze([
    {key: 'topic', label: 'Тема', width: 'minmax(180px, 2.4fr)'},
    {key: 'lectures', label: 'Лек', width: HOURS_COLUMN_WIDTH, isNumeric: true},
    {key: 'practical', label: 'Практ', width: HOURS_COLUMN_WIDTH, isNumeric: true},
    {key: 'laboratory', label: 'Лаб', width: HOURS_COLUMN_WIDTH, isNumeric: true},
    {key: 'consultations', label: 'Конс', width: HOURS_COLUMN_WIDTH, isNumeric: true},
    {key: 'independent', label: 'СРС', width: HOURS_COLUMN_WIDTH, isNumeric: true},
    {key: 'format', label: 'Формат', width: 'minmax(110px, 1fr)'},
    {key: 'assessment', label: 'Оценочное средство', width: 'minmax(130px, 1.4fr)'},
    {key: 'points', label: 'Баллы', width: '64px', isNumeric: true},
]);

/** @type {readonly import('@/core/types/program').TableColumn[]} */
export const SELF_STUDY_COLUMNS = Object.freeze([
    {key: 'topic', label: 'Тема', width: 'minmax(180px, 2fr)'},
    {key: 'semester', label: 'Семестр', width: '80px', isNumeric: true},
    {key: 'deadline', label: 'Срок', width: 'minmax(100px, 1fr)'},
    {key: 'work_type', label: 'Вид работы', width: 'minmax(130px, 1.4fr)'},
    {key: 'hours', label: 'Часы', width: '64px', isNumeric: true},
    {key: 'materials', label: 'Материалы', width: 'minmax(130px, 1.4fr)'},
]);

/** @type {readonly import('@/core/types/program').TableColumn[]} */
export const EQUIPMENT_COLUMNS = Object.freeze([
    {key: 'type', label: 'Вид занятий', width: 'minmax(140px, 1fr)'},
    {key: 'audience', label: 'Аудитория', width: 'minmax(140px, 1fr)'},
    {key: 'equipment', label: 'Оборудование и программы', width: 'minmax(200px, 2fr)'},
]);

/** @type {readonly import('@/core/types/program').TableColumn[]} */
export const ASSESSMENT_CODE_COLUMNS = Object.freeze([
    {key: 'code', label: 'Код компетенции', width: '160px'},
    {key: 'name', label: 'Оценочное средство', width: 'minmax(200px, 1fr)'},
]);

export const ATTESTATION_FORMS = Object.freeze(['зачёт', 'зачёт с оценкой', 'экзамен']);

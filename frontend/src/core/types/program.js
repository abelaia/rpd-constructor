/**
 * @typedef {object} Competency
 * @property {string} id
 * @property {string} competence
 * @property {string} indicator
 * @property {string} knowledge
 * @property {string} skills
 * @property {string} abilities
 */

/**
 * Строка таблицы 4.1 «Содержание дисциплины».
 * @typedef {object} TopicRow
 * @property {string} id
 * @property {string} topic
 * @property {string} lectures
 * @property {string} practical
 * @property {string} laboratory
 * @property {string} consultations
 * @property {string} independent
 * @property {string} format
 * @property {string} assessment
 * @property {string} points
 */

/**
 * Строка таблицы 4.2 «Самостоятельная работа».
 * @typedef {object} SelfStudyRow
 * @property {string} id
 * @property {string} topic
 * @property {string} semester
 * @property {string} deadline
 * @property {string} work_type
 * @property {string} hours
 * @property {string} materials
 */

/**
 * @typedef {object} EquipmentRow
 * @property {string} id
 * @property {string} type
 * @property {string} audience
 * @property {string} equipment
 */

/**
 * @typedef {object} AssessmentCodeRow
 * @property {string} id
 * @property {string} code
 * @property {string} name
 */

/**
 * @typedef {object} LabWork
 * @property {string} id
 * @property {string} goal
 * @property {string} tasks
 * @property {string} theory
 * @property {string} steps
 * @property {string} questions
 */

/**
 * @typedef {object} ProgramSections
 * @property {string} goals раздел I
 * @property {string} position раздел II
 * @property {string} competenciesIntro вводный текст раздела III
 * @property {Competency[]} competencies
 * @property {TopicRow[]} topics таблица 4.1
 * @property {SelfStudyRow[]} selfStudy таблица 4.2
 * @property {string} mainLiterature
 * @property {string} additionalLiterature
 * @property {string} internetResources
 * @property {string} equipmentIntro
 * @property {EquipmentRow[]} equipment
 * @property {string} guidelines раздел VII
 * @property {AssessmentCodeRow[]} assessmentCodes
 * @property {LabWork[]} labs
 * @property {string} finalProvisions раздел IX
 */

/**
 * @typedef {object} Program
 * @property {string} id
 * @property {string} createdAt ISO-дата
 * @property {string} changedAt ISO-дата
 * @property {string} disciplineName
 * @property {string} disciplineNameEn
 * @property {string} code
 * @property {string} semester
 * @property {string} teacherName
 * @property {string} teacherTitle
 * @property {string} department
 * @property {string} umsDate
 * @property {string} umsProtocol
 * @property {string} credits
 * @property {string} totalHours
 * @property {string} attestationForm
 * @property {ProgramSections} sections
 */

/**
 * @typedef {object} SectionInfo
 * @property {string} id
 * @property {string} numeral римский номер, у титульного листа пусто
 * @property {string} title
 * @property {string} shortTitle
 * @property {string} documentTitle заголовок раздела в документе
 * @property {string} hint
 * @property {string} kind значение из SECTION_KINDS
 * @property {keyof ProgramSections} [field] поле текста для разделов вида text
 * @property {string} [placeholder]
 */

/**
 * @typedef {object} TableColumn
 * @property {string} key
 * @property {string} label
 * @property {string} [width] значение для grid-template-columns
 * @property {boolean} [isNumeric]
 */

/**
 * @typedef {object} ProgramCheck
 * @property {string} id
 * @property {string} level значение из CHECK_LEVELS
 * @property {string} title
 * @property {string} hint
 * @property {string} sectionId
 */

/**
 * @typedef {object} NewProgramForm
 * @property {string} name
 * @property {string} mode значение из START_MODES
 * @property {string} [sourceId]
 */

export {};

<script setup>
import {computed} from 'vue';
import {MAX_POINTS, SECTION_KINDS} from '@/core/constants';
import {getPreviewLines} from '@/core/utils/preview';
import {getCompetencyResults, getHoursTotals, getPointsTotal} from '@/core/utils/programs';

const EMPTY_MARK = '____________';
const CURRENT_YEAR = new Date().getFullYear();
const LITERATURE_GROUPS = Object.freeze([
    {key: 'mainLiterature', title: 'Основная литература'},
    {key: 'additionalLiterature', title: 'Дополнительная литература'},
    {key: 'internetResources', title: 'Интернет-ресурсы'},
]);

const props = defineProps({
    /** @type {import('vue').PropType<import('@/core/types/program').Program>} */
    program: {type: Object, required: true},
    /** @type {import('vue').PropType<import('@/core/types/program').SectionInfo>} */
    section: {type: Object, required: true},
});

const sections = computed(() => props.program.sections);
const heading = computed(() => `${props.section.numeral}. ${props.section.documentTitle}`.toUpperCase());
const textLines = computed(() => (props.section.field ? getPreviewLines(sections.value[props.section.field]) : []));
const competencies = computed(() =>
    sections.value.competencies.map((competency) => ({
        ...competency,
        results: getPreviewLines(getCompetencyResults(competency)),
    })),
);
const topics = computed(() => sections.value.topics.map((topic) => ({...topic, hours: getHoursTotals([topic]).total})));
const hours = computed(() => getHoursTotals(sections.value.topics));
const points = computed(() => getPointsTotal(sections.value.topics));
const literature = computed(() =>
    LITERATURE_GROUPS.map((group) => ({...group, lines: getPreviewLines(sections.value[group.key])})).filter(
        (group) => group.lines.length > 0,
    ),
);
const signature = computed(() => props.program.teacherName || EMPTY_MARK);
</script>

<template>
    <div class="editor-preview">
        <article class="editor-preview__paper">
            <template v-if="section.kind === SECTION_KINDS.title">
                <p class="editor-preview__center editor-preview__small">МИНОБРНАУКИ РОССИИ</p>
                <p class="editor-preview__center">Кафедра {{ program.department || EMPTY_MARK }}</p>
                <p class="editor-preview__right editor-preview__small">
                    УТВЕРЖДЕНО
                    <br />
                    протокол УМС № {{ program.umsProtocol || '___' }}
                    <br />
                    от {{ program.umsDate || EMPTY_MARK }}
                </p>
                <p class="editor-preview__center editor-preview__bold editor-preview__gap">
                    РАБОЧАЯ ПРОГРАММА ДИСЦИПЛИНЫ (МОДУЛЯ)
                </p>
                <div class="editor-preview__highlight editor-preview__center">
                    <p class="editor-preview__bold editor-preview__large">{{ program.disciplineName || EMPTY_MARK }}</p>
                    <p
                        v-if="program.disciplineNameEn"
                        class="editor-preview__italic"
                    >
                        {{ program.disciplineNameEn }}
                    </p>
                </div>
                <p
                    v-if="program.code"
                    class="editor-preview__center"
                >
                    Код дисциплины: {{ program.code }}
                </p>
                <p class="editor-preview__gap">
                    Составитель:
                    <br />
                    {{ signature }}, {{ program.teacherTitle || EMPTY_MARK }}
                </p>
                <p class="editor-preview__center editor-preview__bottom">{{ CURRENT_YEAR }}</p>
            </template>
            <template v-else>
                <p class="editor-preview__center editor-preview__bold">{{ heading }}</p>
                <div class="editor-preview__highlight">
                    <template v-if="section.kind === SECTION_KINDS.text">
                        <p
                            v-for="line in textLines"
                            :key="line.id"
                            :class="line.isListItem ? 'editor-preview__item' : 'editor-preview__paragraph'"
                        >
                            {{ line.text }}
                        </p>
                    </template>
                    <template v-else-if="section.kind === SECTION_KINDS.competencies">
                        <p
                            v-if="sections.competenciesIntro"
                            class="editor-preview__paragraph"
                        >
                            {{ sections.competenciesIntro }}
                        </p>
                        <div
                            v-for="competency in competencies"
                            :key="competency.id"
                            class="editor-preview__group"
                        >
                            <p class="editor-preview__bold">{{ competency.competence || EMPTY_MARK }}</p>
                            <p>{{ competency.indicator }}</p>
                            <p
                                v-for="line in competency.results"
                                :key="line.id"
                                class="editor-preview__italic"
                            >
                                {{ line.text }}
                            </p>
                        </div>
                    </template>
                    <template v-else-if="section.kind === SECTION_KINDS.content">
                        <p class="editor-preview__paragraph">
                            Общая трудоёмкость дисциплины — {{ program.credits }} з. е. ({{ program.totalHours }} ч.),
                            форма аттестации — {{ program.attestationForm }}.
                        </p>
                        <table class="editor-preview__table">
                            <thead>
                                <tr>
                                    <th>№</th>
                                    <th>Тема</th>
                                    <th>Ч.</th>
                                    <th>Б.</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr
                                    v-for="(topic, index) in topics"
                                    :key="topic.id"
                                >
                                    <td>{{ index + 1 }}</td>
                                    <td>{{ topic.topic }}</td>
                                    <td>{{ topic.hours }}</td>
                                    <td>{{ topic.points }}</td>
                                </tr>
                                <tr class="editor-preview__total">
                                    <td />
                                    <td>Итого</td>
                                    <td>{{ hours.total }}</td>
                                    <td>{{ points }}/{{ MAX_POINTS }}</td>
                                </tr>
                            </tbody>
                        </table>
                    </template>
                    <template v-else-if="section.kind === SECTION_KINDS.literature">
                        <div
                            v-for="group in literature"
                            :key="group.key"
                            class="editor-preview__group"
                        >
                            <p class="editor-preview__bold">{{ group.title }}</p>
                            <p
                                v-for="line in group.lines"
                                :key="line.id"
                            >
                                {{ line.text }}
                            </p>
                        </div>
                    </template>
                    <template v-else-if="section.kind === SECTION_KINDS.equipment">
                        <p class="editor-preview__paragraph">{{ sections.equipmentIntro }}</p>
                        <p
                            v-for="(row, index) in sections.equipment"
                            :key="row.id"
                        >
                            {{ index + 1 }}. {{ [row.type, row.audience, row.equipment].filter(Boolean).join(' — ') }}
                        </p>
                    </template>
                    <template v-else>
                        <div
                            v-for="(lab, index) in sections.labs"
                            :key="lab.id"
                            class="editor-preview__group"
                        >
                            <p class="editor-preview__bold">Лабораторная работа № {{ index + 1 }}</p>
                            <p>
                                <b>Цель работы:</b>
                                {{ lab.goal || EMPTY_MARK }}
                            </p>
                            <p v-if="lab.tasks">
                                <b>Задачи:</b>
                                {{ lab.tasks }}
                            </p>
                        </div>
                    </template>
                </div>
            </template>
        </article>
        <p class="editor-preview__note">Обновляется по мере ввода</p>
    </div>
</template>

<style lang="scss">
$paper-min-height: 560px;

.editor-preview {
    @include column($indent-step * 3);

    &__paper {
        overflow: hidden;
        min-height: $paper-min-height;
        transform: rotate(1deg);
        overflow-wrap: anywhere;

        @include paper;
        @include column($indent-step * 3);
        @include padding('y', 7);
        @include padding('x', 6);
    }

    &__center {
        text-align: center;
    }

    &__right {
        text-align: right;
    }

    &__small {
        font-size: $font-size-xs;
        line-height: 1.5;
    }

    &__large {
        font-size: $font-size-md + 1px;
    }

    &__bold {
        font-weight: $font-weight-bold;
    }

    &__italic {
        font-style: italic;
    }

    &__gap {
        margin-top: $indent-step * 4;
    }

    &__bottom {
        margin-top: auto;
    }

    &__highlight {
        margin: 0 (-$indent-step * 2.5);
        border-radius: 0 $indent-step * 1.5 $indent-step * 1.5 0;
        background-color: $color-honey;
        box-shadow: -4px 0 0 $color-amber;

        @include column($indent-step * 2);
        @include padding('y', 1.5);
        @include padding('x', 2.5);
    }

    &__paragraph {
        text-align: justify;
        text-indent: $indent-step * 6;
    }

    &__item {
        position: relative;

        @include padding('left', 4);

        &::before {
            position: absolute;
            left: 0;
            content: '–';
        }
    }

    &__group {
        @include column($indent-step);
    }

    &__table {
        width: 100%;
        border-collapse: collapse;
        font-size: $font-size-xs;
        line-height: 1.35;

        th,
        td {
            vertical-align: top;
            text-align: left;
            border: 1px solid rgba($color-paper-ink, 35%);

            @include padding('y', 1);
            @include padding('x', 1.5);
        }
    }

    &__total {
        font-weight: $font-weight-bold;
    }

    &__note {
        text-align: center;

        @include caption;
    }
}
</style>

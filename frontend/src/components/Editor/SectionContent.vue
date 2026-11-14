<script setup>
import {computed} from 'vue';
import {CHECK_LEVELS, MAX_POINTS} from '@/core/constants';
import {ATTESTATION_FORMS, SELF_STUDY_COLUMNS, TOPIC_COLUMNS} from '@/core/data/tables';
import {getChecks, getHoursTotals, getPointsTotal} from '@/core/utils/programs';

import EditorTable from '@/components/Editor/EditorTable.vue';
import UiField from '@/components/Ui/UiField.vue';
import UiProgress from '@/components/Ui/UiProgress.vue';
import UiSelect from '@/components/Ui/UiSelect.vue';

const props = defineProps({
    /** @type {import('vue').PropType<import('@/core/types/program').Program>} */
    program: {type: Object, required: true},
});

const emit = defineEmits(['update', 'update-sections']);

const hours = computed(() => getHoursTotals(props.program.sections.topics));
const points = computed(() => getPointsTotal(props.program.sections.topics));
const totals = computed(() => ({
    topic: 'Итого',
    lectures: String(hours.value.lectures),
    practical: String(hours.value.practical),
    laboratory: String(hours.value.laboratory),
    consultations: String(hours.value.consultations),
    independent: String(hours.value.independent),
    points: `${points.value} / ${MAX_POINTS}`,
}));
const sumChecks = computed(() => getChecks(props.program).filter((check) => check.sectionId === 'IV'));
const summaryLevel = computed(() => {
    const levels = sumChecks.value.map((check) => check.level);

    if (levels.includes(CHECK_LEVELS.error)) {
        return CHECK_LEVELS.error;
    }

    return levels.includes(CHECK_LEVELS.warning) ? CHECK_LEVELS.warning : CHECK_LEVELS.ok;
});
</script>

<template>
    <div class="section-content">
        <div class="section-content__plan">
            <UiField
                :model-value="program.credits"
                label="Зачётные единицы"
                inputmode="numeric"
                is-numeric
                @update:model-value="emit('update', {credits: $event})"
            />
            <UiField
                :model-value="program.totalHours"
                label="Часы по плану"
                inputmode="numeric"
                is-numeric
                @update:model-value="emit('update', {totalHours: $event})"
            />
            <UiSelect
                :model-value="program.attestationForm"
                label="Форма аттестации"
                :options="ATTESTATION_FORMS"
                @update:model-value="emit('update', {attestationForm: $event})"
            />
        </div>
        <section class="section-content__block">
            <h3 class="section-content__subtitle">4.1. Темы, часы и баллы</h3>
            <EditorTable
                caption="Темы дисциплины"
                item-label="Тема"
                add-label="Добавить тему"
                :columns="TOPIC_COLUMNS"
                :rows="program.sections.topics"
                :totals="totals"
                @update:rows="emit('update-sections', {topics: $event})"
            />
            <div
                v-if="program.sections.topics.length > 0"
                :class="['section-content__summary', `section-content__summary--${summaryLevel}`]"
                role="status"
            >
                <span class="section-content__summary-points">
                    Баллы: {{ points }} из {{ MAX_POINTS }}
                    <UiProgress
                        class="section-content__summary-bar"
                        :value="points"
                        :label="`Распределено ${points} баллов из ${MAX_POINTS}`"
                    />
                </span>
                <span
                    v-for="check in sumChecks"
                    :key="check.id"
                >
                    {{ check.hint }}
                </span>
            </div>
        </section>
        <section class="section-content__block">
            <h3 class="section-content__subtitle">4.2. Самостоятельная работа</h3>
            <EditorTable
                caption="Самостоятельная работа"
                item-label="Работа"
                add-label="Добавить работу"
                :columns="SELF_STUDY_COLUMNS"
                :rows="program.sections.selfStudy"
                @update:rows="emit('update-sections', {selfStudy: $event})"
            />
        </section>
    </div>
</template>

<style lang="scss">
$plan-field-width: 160px;
$plan-select-width: 240px;
$summary-bar-width: 160px;

.section-content {
    @include column($indent-step * 6);

    &__plan {
        display: grid;
        grid-template-columns: $plan-field-width $plan-field-width minmax(0, $plan-select-width);
        gap: $indent-step * 4;
    }

    &__block {
        @include column($indent-step * 3);
    }

    &__subtitle {
        font-size: $font-size-lg;
        font-weight: $font-weight-semibold;
    }

    &__summary {
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        border-radius: $radius-panel;
        font-size: $font-size-sm + 1px;
        font-variant-numeric: tabular-nums;
        gap: ($indent-step * 2) ($indent-step * 6);

        @include padding('y', 3);
        @include padding('x', 4);

        &--ok {
            color: $color-teal;
            background-color: $color-mint;
        }

        &--warning {
            color: $color-honey-ink;
            background-color: $color-honey;
        }

        &--error {
            color: $color-danger;
            background-color: $color-danger-surface;
        }
    }

    &__summary-points {
        display: flex;
        align-items: center;
        font-weight: $font-weight-extrabold;
        gap: $indent-step * 3;
    }

    &__summary-bar {
        width: $summary-bar-width;
    }

    @include mobile {
        &__plan {
            grid-template-columns: repeat(2, minmax(0, 1fr));

            .ui-select {
                grid-column: 1 / -1;
            }
        }
    }
}
</style>

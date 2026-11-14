<script setup>
import {computed} from 'vue';
import {AccordionContent, AccordionHeader, AccordionItem, AccordionRoot, AccordionTrigger} from 'reka-ui';
import {ChevronDown, Plus, Trash2} from 'lucide-vue-next';
import {ASSESSMENT_CODE_COLUMNS} from '@/core/data/tables';
import {createId} from '@/core/helpers/createId';
import {createRow, removeRow, updateRow} from '@/core/utils/rows';

import EditorTable from '@/components/Editor/EditorTable.vue';
import UiButton from '@/components/Ui/UiButton.vue';
import UiField from '@/components/Ui/UiField.vue';

const LAB_FIELDS = Object.freeze([
    {key: 'goal', label: 'Цель', rows: 2, isWide: true},
    {key: 'tasks', label: 'Задание', rows: 5, hint: 'Что именно студент должен сдать'},
    {key: 'steps', label: 'Порядок выполнения', rows: 5, hint: 'По шагам, каждый с новой строки'},
    {key: 'theory', label: 'Теоретические сведения', rows: 4},
    {key: 'questions', label: 'Контрольные вопросы', rows: 4},
]);
const LAB_KEYS = Object.freeze(LAB_FIELDS.map((field) => field.key));
const REQUIRED_LAB_KEYS = Object.freeze(['goal', 'tasks', 'steps']);

const props = defineProps({
    /** @type {import('vue').PropType<import('@/core/types/program').Program>} */
    program: {type: Object, required: true},
});

const emit = defineEmits(['update', 'update-sections']);

const labs = computed(() =>
    props.program.sections.labs.map((lab) => ({
        ...lab,
        isFilled: REQUIRED_LAB_KEYS.every((key) => lab[key].trim() !== ''),
    })),
);
const firstLabId = computed(() => props.program.sections.labs[0]?.id);

/** @param {import('@/core/types/program').LabWork[]} nextLabs */
function save(nextLabs) {
    emit('update-sections', {labs: nextLabs});
}

/**
 * @param {string} id
 * @param {string} key
 * @param {string} value
 */
function handleUpdate(id, key, value) {
    save(updateRow(props.program.sections.labs, id, key, value));
}

function handleAdd() {
    save([...props.program.sections.labs, createRow(createId(), LAB_KEYS)]);
}

/** @param {string} id */
function handleRemove(id) {
    save(removeRow(props.program.sections.labs, id));
}
</script>

<template>
    <div class="section-assessment">
        <section class="section-assessment__block">
            <h3 class="section-assessment__subtitle">Оценочные средства по компетенциям</h3>
            <EditorTable
                caption="Оценочные средства по компетенциям"
                item-label="Строка"
                add-label="Добавить строку"
                :columns="ASSESSMENT_CODE_COLUMNS"
                :rows="program.sections.assessmentCodes"
                @update:rows="emit('update-sections', {assessmentCodes: $event})"
            />
        </section>
        <section class="section-assessment__block">
            <div class="section-assessment__head">
                <h3 class="section-assessment__subtitle">Лабораторные работы</h3>
                <span class="section-assessment__count">{{ labs.length }}</span>
            </div>
            <AccordionRoot
                class="section-assessment__labs"
                type="single"
                :default-value="firstLabId"
                collapsible
            >
                <AccordionItem
                    v-for="(lab, index) in labs"
                    :key="lab.id"
                    :value="lab.id"
                    class="section-assessment__lab"
                >
                    <AccordionHeader class="section-assessment__lab-header">
                        <AccordionTrigger class="section-assessment__trigger">
                            <ChevronDown
                                class="section-assessment__chevron"
                                :size="20"
                                aria-hidden="true"
                            />
                            <span class="section-assessment__lab-title">Лабораторная работа № {{ index + 1 }}</span>
                            <span
                                :class="[
                                    'section-assessment__status',
                                    {'section-assessment__status--done': lab.isFilled},
                                ]"
                            >
                                {{ lab.isFilled ? 'Заполнена' : 'В работе' }}
                            </span>
                        </AccordionTrigger>
                        <button
                            type="button"
                            class="section-assessment__remove"
                            :aria-label="`Удалить лабораторную работу № ${index + 1}`"
                            @click="handleRemove(lab.id)"
                        >
                            <Trash2
                                :size="18"
                                aria-hidden="true"
                            />
                        </button>
                    </AccordionHeader>
                    <AccordionContent class="section-assessment__content">
                        <div class="section-assessment__fields">
                            <UiField
                                v-for="field in LAB_FIELDS"
                                :key="field.key"
                                :class="{'section-assessment__wide': field.isWide}"
                                :model-value="lab[field.key]"
                                :label="field.label"
                                :hint="field.hint ?? ''"
                                :rows="field.rows"
                                @update:model-value="handleUpdate(lab.id, field.key, $event)"
                            />
                        </div>
                    </AccordionContent>
                </AccordionItem>
            </AccordionRoot>
            <UiButton
                theme="outline"
                class="section-assessment__add"
                @click="handleAdd"
            >
                <Plus
                    :size="18"
                    aria-hidden="true"
                />
                Добавить работу
            </UiButton>
        </section>
    </div>
</template>

<style lang="scss">
$trigger-height: 56px;

.section-assessment {
    @include column($indent-step * 8);

    &__block {
        @include column($indent-step * 3);
    }

    &__head {
        display: flex;
        align-items: center;
        gap: $indent-step * 2;
    }

    &__subtitle {
        font-size: $font-size-lg;
        font-weight: $font-weight-semibold;
    }

    &__count {
        color: $color-ink-soft;
        font-weight: $font-weight-bold;
        font-variant-numeric: tabular-nums;
    }

    &__labs {
        @include column($indent-step * 3);
    }

    &__lab {
        border: 1px solid $color-line;
        border-radius: $radius-panel;
        background-color: $color-surface;

        &[data-state='open'] {
            border-color: $color-mint-line;
        }
    }

    &__lab-header {
        display: flex;
        align-items: center;
        margin: 0;

        @include padding('right', 2);
    }

    &__trigger {
        display: flex;
        align-items: center;
        flex: 1;
        min-height: $trigger-height;
        text-align: left;
        border-radius: $radius-panel;
        font-weight: $font-weight-bold;
        gap: $indent-step * 3;

        @include button-reset;
        @include padding('x', 4);

        &[data-state='open'] .section-assessment__chevron {
            transform: rotate(180deg);
        }
    }

    &__chevron {
        flex: none;
        transition: transform $duration ease;
    }

    &__lab-title {
        flex: 1;
    }

    &__status {
        @include chip-status($color-honey, $color-honey-ink);

        &--done {
            color: $color-teal;
            background-color: $color-mint;
        }
    }

    &__remove {
        @include icon-button;
    }

    &__content {
        overflow: hidden;
    }

    &__fields {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: ($indent-step * 4) ($indent-step * 5);

        @include padding('top', 1);
        @include padding('x', 4);
        @include padding('bottom', 5);
    }

    &__wide {
        grid-column: 1 / -1;
    }

    &__add {
        align-self: flex-start;
    }

    @include mobile {
        &__fields {
            grid-template-columns: minmax(0, 1fr);
        }
    }
}
</style>

<script setup>
import {computed} from 'vue';
import {Plus, Trash2} from 'lucide-vue-next';
import {COMPETENCY_CATALOG} from '@/core/data/catalog';
import {createId} from '@/core/helpers/createId';
import {createRow, removeRow, updateRow} from '@/core/utils/rows';

import UiButton from '@/components/Ui/UiButton.vue';
import UiField from '@/components/Ui/UiField.vue';

const COMPETENCY_KEYS = Object.freeze(['competence', 'indicator', 'knowledge', 'skills', 'abilities']);
const RESULT_FIELDS = Object.freeze([
    {key: 'knowledge', label: 'Знания', placeholder: 'Что студент будет знать'},
    {key: 'skills', label: 'Умения', placeholder: 'Что студент будет уметь'},
    {key: 'abilities', label: 'Навыки', placeholder: 'Чем студент будет владеть'},
]);
const RESULT_ROWS = 4;
const INTRO_ROWS = 3;

const COMPETENCY_OPTIONS = Object.freeze(COMPETENCY_CATALOG.map((item) => `${item.code}. ${item.title}`));

const props = defineProps({
    /** @type {import('vue').PropType<import('@/core/types/program').Program>} */
    program: {type: Object, required: true},
});

const emit = defineEmits(['update', 'update-sections']);

const competencies = computed(() =>
    props.program.sections.competencies.map((competency) => {
        const catalogItem = COMPETENCY_CATALOG.find((item) => competency.competence.startsWith(item.code));

        return {
            ...competency,
            code: catalogItem?.code ?? '',
            indicatorOptions: catalogItem?.indicators ?? [],
        };
    }),
);

/** @param {import('@/core/types/program').Competency[]} nextCompetencies */
function save(nextCompetencies) {
    emit('update-sections', {competencies: nextCompetencies});
}

/**
 * @param {string} id
 * @param {string} key
 * @param {string} value
 */
function handleUpdate(id, key, value) {
    save(updateRow(props.program.sections.competencies, id, key, value));
}

function handleAdd() {
    save([...props.program.sections.competencies, createRow(createId(), COMPETENCY_KEYS)]);
}

/** @param {string} id */
function handleRemove(id) {
    save(removeRow(props.program.sections.competencies, id));
}
</script>

<template>
    <div class="section-competencies">
        <UiField
            :model-value="program.sections.competenciesIntro"
            label="Вводный текст"
            placeholder="Процесс изучения дисциплины направлен на формирование следующих компетенций:"
            :rows="INTRO_ROWS"
            @update:model-value="emit('update-sections', {competenciesIntro: $event})"
        />
        <article
            v-for="(competency, index) in competencies"
            :key="competency.id"
            class="section-competencies__card"
        >
            <div class="section-competencies__head">
                <span :class="['section-competencies__code', {'section-competencies__code--empty': !competency.code}]">
                    {{ competency.code || 'Не выбрана' }}
                </span>
                <h3 class="section-competencies__title">Компетенция {{ index + 1 }}</h3>
                <button
                    type="button"
                    class="section-competencies__remove"
                    :aria-label="`Удалить компетенцию ${index + 1}`"
                    @click="handleRemove(competency.id)"
                >
                    <Trash2
                        :size="18"
                        aria-hidden="true"
                    />
                </button>
            </div>
            <UiField
                :model-value="competency.competence"
                label="Компетенция"
                hint="Начните вводить код или название — подскажем из справочника"
                :suggestions="COMPETENCY_OPTIONS"
                @update:model-value="handleUpdate(competency.id, 'competence', $event)"
            />
            <div class="section-competencies__nested">
                <UiField
                    :model-value="competency.indicator"
                    label="Индикатор"
                    :suggestions="competency.indicatorOptions"
                    @update:model-value="handleUpdate(competency.id, 'indicator', $event)"
                />
                <div class="section-competencies__results">
                    <UiField
                        v-for="field in RESULT_FIELDS"
                        :key="field.key"
                        :model-value="competency[field.key]"
                        :label="field.label"
                        :placeholder="field.placeholder"
                        :rows="RESULT_ROWS"
                        @update:model-value="handleUpdate(competency.id, field.key, $event)"
                    />
                </div>
            </div>
        </article>
        <UiButton
            theme="outline"
            class="section-competencies__add"
            @click="handleAdd"
        >
            <Plus
                :size="18"
                aria-hidden="true"
            />
            Добавить компетенцию
        </UiButton>
    </div>
</template>

<style lang="scss">
.section-competencies {
    @include column($indent-step * 4);

    &__card {
        border: 1px solid $color-line;
        border-radius: $radius-tile;

        @include column($indent-step * 3);
        @include padding('y', 4);
        @include padding('x', 5);
    }

    &__head {
        display: flex;
        align-items: center;
        gap: $indent-step * 3;
    }

    &__code {
        @include chip-status($color-mint, $color-teal);

        &--empty {
            color: $color-honey-ink;
            background-color: $color-honey;
        }
    }

    &__title {
        flex: 1;
        font-size: $font-size-lg;
        font-weight: $font-weight-semibold;
    }

    &__remove {
        @include icon-button;
    }

    &__nested {
        border-left: 2px solid $color-mint-line;

        @include column($indent-step * 3);
        @include padding('left', 4);
        @include margin('left', 2);
    }

    &__results {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: $indent-step * 3;
    }

    &__add {
        align-self: flex-start;
    }
}
</style>

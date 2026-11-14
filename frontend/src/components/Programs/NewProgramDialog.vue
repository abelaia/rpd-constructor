<script setup>
import {computed} from 'vue';
import {CopyPlus, FilePlus2, LayoutTemplate} from 'lucide-vue-next';
import {PROGRAM_NAME_MAX_LENGTH, START_MODES} from '@/core/constants';
import {useNewProgramForm} from '@/composables/useNewProgramForm';

import UiButton from '@/components/Ui/UiButton.vue';
import UiField from '@/components/Ui/UiField.vue';
import UiModal from '@/components/Ui/UiModal.vue';

const MODES = Object.freeze([
    {mode: START_MODES.blank, title: 'С нуля', text: 'Пустые разделы I–IX', icon: FilePlus2},
    {mode: START_MODES.copy, title: 'На основе моей программы', text: 'Копия с вашими текстами', icon: CopyPlus},
    {
        mode: START_MODES.template,
        title: 'Из шаблона кафедры',
        text: 'Общие разделы уже заполнены',
        icon: LayoutTemplate,
    },
]);

const props = defineProps({
    initialMode: {
        type: String,
        default: START_MODES.blank,
        validator: (value) => Object.values(START_MODES).includes(value),
    },
    /** @type {import('vue').PropType<import('@/core/types/program').Program[]>} */
    programs: {type: Array, required: true},
});

const emit = defineEmits(['close', 'created']);

const {name, mode, sourceId, nameError, sourceError, submit} = useNewProgramForm(props.initialMode, (program) =>
    emit('created', program),
);

const modes = computed(() =>
    MODES.map((item) => ({...item, isDisabled: item.mode === START_MODES.copy && props.programs.length === 0})),
);
const isCopyMode = computed(() => mode.value === START_MODES.copy);
</script>

<template>
    <UiModal
        title="Новая программа"
        description="Название можно будет изменить позже."
        is-wide
        @close="emit('close')"
    >
        <form
            class="new-program"
            @submit.prevent="submit"
        >
            <UiField
                v-model="name"
                label="Название дисциплины"
                hint="Как в учебном плане, например: «Базы данных»"
                :error="nameError"
                :maxlength="PROGRAM_NAME_MAX_LENGTH"
                autofocus
            />
            <fieldset class="new-program__modes">
                <legend class="new-program__legend">С чего начать</legend>
                <label
                    v-for="item in modes"
                    :key="item.mode"
                    :class="[
                        'new-program__mode',
                        {
                            'new-program__mode--active': mode === item.mode,
                            'new-program__mode--disabled': item.isDisabled,
                        },
                    ]"
                >
                    <input
                        v-model="mode"
                        class="new-program__radio"
                        type="radio"
                        name="start-mode"
                        :value="item.mode"
                        :disabled="item.isDisabled"
                    />
                    <span class="new-program__mode-icon">
                        <component
                            :is="item.icon"
                            :size="28"
                            aria-hidden="true"
                        />
                    </span>
                    <span class="new-program__mode-title">{{ item.title }}</span>
                    <span class="new-program__mode-text">{{ item.text }}</span>
                </label>
            </fieldset>
            <div
                v-if="isCopyMode"
                class="new-program__source"
            >
                <label
                    class="new-program__legend"
                    for="new-program-source"
                >
                    Какую программу взять за основу
                </label>
                <select
                    id="new-program-source"
                    v-model="sourceId"
                    class="new-program__select"
                    :aria-invalid="Boolean(sourceError)"
                >
                    <option
                        value=""
                        disabled
                    >
                        Выберите программу
                    </option>
                    <option
                        v-for="program in programs"
                        :key="program.id"
                        :value="program.id"
                    >
                        {{ program.disciplineName }}
                    </option>
                </select>
                <p
                    v-if="sourceError"
                    class="new-program__error"
                    role="alert"
                >
                    {{ sourceError }}
                </p>
            </div>
            <div class="new-program__actions">
                <UiButton
                    theme="text"
                    @click="emit('close')"
                >
                    Отмена
                </UiButton>
                <UiButton type="submit">Создать</UiButton>
            </div>
        </form>
    </UiModal>
</template>

<style lang="scss">
$mode-icon-size: 64px;

.new-program {
    @include column($indent-step * 6);

    &__modes {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        margin: 0;
        padding: 0;
        border: none;
        gap: $indent-step * 3;
    }

    &__legend {
        margin-bottom: $indent-step * 2;
        padding: 0;
        color: $color-ink-soft;
        font-size: $font-size-sm;
        font-weight: $font-weight-semibold;
    }

    &__mode {
        position: relative;
        cursor: pointer;
        transition:
            border-color $duration ease,
            background-color $duration ease;
        border: 1.5px solid $color-line-strong;
        border-radius: $radius-tile;

        @include column($indent-step * 2);
        @include padding('y', 4);
        @include padding('x', 4);

        @include hover {
            border-color: $color-teal-light;
        }

        &:focus-within {
            outline: 2px solid $color-teal;
            outline-offset: 2px;
        }

        &--active {
            border-color: $color-teal;
            background-color: $color-mint;
        }

        &--disabled {
            cursor: not-allowed;
            opacity: 0.55;
        }
    }

    &__radio {
        position: absolute;
        opacity: 0;
    }

    &__mode-icon {
        width: $mode-icon-size;
        height: $mode-icon-size;
        color: $color-teal;
        border-radius: $radius-tile;
        background-color: $color-surface-muted;

        @include flex-center;
    }

    &__mode-title {
        font-size: $font-size-sm + 1px;
        font-weight: $font-weight-bold;
        line-height: 1.3;
    }

    &__mode-text {
        color: $color-ink-soft;
        font-size: $font-size-xs;
        line-height: 1.35;
    }

    &__source {
        display: flex;
        flex-direction: column;
    }

    &__select {
        height: $control-height;
        cursor: pointer;

        @include control;
    }

    &__error {
        margin-top: $indent-step * 1.5;
        color: $color-danger;
        font-size: $font-size-xs;
        font-weight: $font-weight-semibold;
    }

    &__actions {
        display: flex;
        justify-content: flex-end;
        gap: $indent-step * 2;
    }

    @include mobile {
        &__modes {
            grid-template-columns: minmax(0, 1fr);
        }
    }
}
</style>

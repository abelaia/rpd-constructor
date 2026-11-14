<script setup>
import {computed, useId} from 'vue';

const props = defineProps({
    label: {type: String, required: true},
    type: {type: String, default: 'text'},
    placeholder: {type: String, default: ''},
    maxlength: {type: Number, default: undefined},
    inputmode: {type: String, default: undefined},
    /** @type {import('vue').PropType<readonly string[]>} */
    suggestions: {type: Array, default: () => []},
    rows: {type: Number, default: 0},
    error: {type: String, default: null},
    hint: {type: String, default: ''},
    isNumeric: {type: Boolean, default: false},
    autofocus: {type: Boolean, default: false},
});

const model = defineModel({type: String, default: ''});

const fieldId = useId();

const isMultiline = computed(() => props.rows > 0);
const hasNote = computed(() => Boolean(props.error || props.hint));
const describedBy = computed(() => (hasNote.value ? `${fieldId}-note` : undefined));
const listId = computed(() => (props.suggestions.length > 0 ? `${fieldId}-list` : undefined));
const controlClass = computed(() => [
    'ui-field__control',
    {
        'ui-field__control--multiline': isMultiline.value,
        'ui-field__control--numeric': props.isNumeric,
        'ui-field__control--error': props.error,
    },
]);
</script>

<template>
    <div class="ui-field">
        <label
            class="ui-field__label"
            :for="fieldId"
        >
            {{ label }}
        </label>
        <textarea
            v-if="isMultiline"
            :id="fieldId"
            v-model="model"
            :class="controlClass"
            :rows="rows"
            :placeholder="placeholder"
            :aria-invalid="Boolean(error)"
            :aria-describedby="describedBy"
        />
        <input
            v-else
            :id="fieldId"
            v-model="model"
            :class="controlClass"
            :type="type"
            :placeholder="placeholder"
            :maxlength="maxlength"
            :inputmode="inputmode"
            :list="listId"
            :aria-invalid="Boolean(error)"
            :aria-describedby="describedBy"
            :autofocus="autofocus"
        />
        <datalist
            v-if="listId"
            :id="listId"
        >
            <option
                v-for="suggestion in suggestions"
                :key="suggestion"
                :value="suggestion"
            />
        </datalist>
        <p
            v-if="hasNote"
            :id="`${fieldId}-note`"
            :class="['ui-field__note', {'ui-field__note--error': error}]"
            :role="error ? 'alert' : undefined"
        >
            {{ error ?? hint }}
        </p>
    </div>
</template>

<style lang="scss">
.ui-field {
    min-width: 0;

    @include column($indent-step * 1.5);

    &__label {
        color: $color-ink-soft;
        font-size: $font-size-sm;
        font-weight: $font-weight-semibold;
        line-height: 1.4;
    }

    &__control {
        height: $control-height;

        @include control;

        &--multiline {
            display: block;
            height: auto;
            resize: vertical;
            line-height: 1.47;

            @include padding('y', 2.5);
        }

        &--numeric {
            font-variant-numeric: tabular-nums;
        }

        &--error {
            border-color: $color-danger;
            box-shadow: 0 0 0 1px $color-danger;
        }
    }

    &__note {
        color: $color-ink-soft;
        font-size: $font-size-xs;
        line-height: 1.35;

        &--error {
            color: $color-danger;
            font-weight: $font-weight-semibold;
        }
    }
}
</style>

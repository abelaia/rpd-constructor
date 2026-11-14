<script setup>
import {useId} from 'vue';
import {ChevronDown} from 'lucide-vue-next';

defineProps({
    label: {type: String, required: true},
    /** @type {import('vue').PropType<readonly string[]>} */
    options: {type: Array, required: true},
});

const model = defineModel({type: String, default: ''});

const fieldId = useId();
</script>

<template>
    <div class="ui-select">
        <label
            class="ui-select__label"
            :for="fieldId"
        >
            {{ label }}
        </label>
        <span class="ui-select__box">
            <select
                :id="fieldId"
                v-model="model"
                class="ui-select__control"
            >
                <option
                    v-for="option in options"
                    :key="option"
                    :value="option"
                >
                    {{ option }}
                </option>
            </select>
            <ChevronDown
                class="ui-select__icon"
                :size="16"
                aria-hidden="true"
            />
        </span>
    </div>
</template>

<style lang="scss">
.ui-select {
    min-width: 0;

    @include column($indent-step * 1.5);

    &__label {
        color: $color-ink-soft;
        font-size: $font-size-sm;
        font-weight: $font-weight-semibold;
        line-height: 1.4;
    }

    &__box {
        position: relative;
        display: block;
    }

    &__control {
        height: $control-height;
        cursor: pointer;
        appearance: none;

        @include control;
        @include padding('right', 9);
    }

    &__icon {
        position: absolute;
        top: 50%;
        right: $indent-step * 3.5;
        transform: translateY(-50%);
        pointer-events: none;
        color: $color-ink-soft;
    }
}
</style>

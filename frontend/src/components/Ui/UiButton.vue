<script setup>
import {computed} from 'vue';
import {RouterLink} from 'vue-router';

const props = defineProps({
    theme: {
        type: String,
        default: 'primary',
        validator: (value) => ['primary', 'secondary', 'outline', 'text', 'danger', 'inverse'].includes(value),
    },
    size: {
        type: String,
        default: 'medium',
        validator: (value) => ['small', 'medium', 'large'].includes(value),
    },
    type: {
        type: String,
        default: 'button',
        validator: (value) => ['button', 'submit'].includes(value),
    },
    /** @type {import('vue').PropType<import('vue-router').RouteLocationRaw | null>} */
    to: {type: Object, default: null},
    isFluid: {type: Boolean, default: false},
    isLoading: {type: Boolean, default: false},
    disabled: {type: Boolean, default: false},
});

const emit = defineEmits(['click']);

const rootClass = computed(() => [
    'ui-button',
    `ui-button--${props.theme}`,
    `ui-button--${props.size}`,
    {
        'ui-button--fluid': props.isFluid,
        'ui-button--loading': props.isLoading,
    },
]);
</script>

<template>
    <RouterLink
        v-if="to"
        :class="rootClass"
        :to="to"
    >
        <slot />
    </RouterLink>
    <button
        v-else
        :type="type"
        :class="rootClass"
        :disabled="disabled || isLoading"
        :aria-busy="isLoading"
        @click="emit('click', $event)"
    >
        <slot />
    </button>
</template>

<style lang="scss">
$spinner-size: 16px;
$edge-height: 3px;

.ui-button {
    display: inline-flex;
    align-items: center;
    flex: none;
    justify-content: center;
    height: $control-height;
    transition:
        transform $duration-fast ease,
        background-color $duration ease,
        border-color $duration ease,
        box-shadow $duration ease;
    white-space: nowrap;
    border: 1px solid transparent;
    border-radius: $radius-chip;
    font-size: $font-size-md;
    font-weight: $font-weight-bold;
    line-height: 1;
    gap: $indent-step * 2;

    @include padding('x', 5);

    &:active:not(:disabled) {
        transform: scale(0.98);
    }

    &--small {
        height: $control-height-sm;
        font-size: $font-size-sm;

        @include padding('x', 3.5);
    }

    &--large {
        height: $control-height-lg;
        font-size: $font-size-md + 1px;

        @include padding('x', 7);
    }

    &--fluid {
        width: 100%;
    }

    &--primary {
        color: $color-button-ink;
        background-color: $color-amber;
        box-shadow: 0 $edge-height 0 $color-amber-edge;

        @include hover {
            background-color: $color-amber-hover;
        }

        &:active:not(:disabled) {
            transform: translateY($edge-height - 1px) scale(0.98);
            box-shadow: 0 1px 0 $color-amber-edge;
        }
    }

    &--secondary {
        color: $color-white;
        background-color: $color-teal;
        box-shadow: 0 $edge-height 0 $color-pine-edge;

        @include hover {
            background-color: $color-pine;
        }

        &:active:not(:disabled) {
            transform: translateY($edge-height - 1px) scale(0.98);
            box-shadow: 0 1px 0 $color-pine-edge;
        }
    }

    &--outline {
        color: $color-teal;
        border-color: $color-mint-line;
        background-color: $color-surface;

        @include hover {
            background-color: $color-mint;
        }
    }

    &--text {
        color: $color-teal;
        background-color: transparent;

        @include padding('x', 3);

        @include hover {
            background-color: $color-mint;
        }
    }

    &--danger {
        color: $color-white;
        background-color: $color-danger;

        @include hover {
            background-color: $color-danger-deep;
        }
    }

    &--inverse {
        color: $color-white;
        border-color: rgba($color-white, 50%);
        background-color: transparent;

        @include hover {
            background-color: rgba($color-white, 12%);
        }

        &:focus-visible {
            outline-color: $color-white;
        }
    }

    &--loading::before {
        width: $spinner-size;
        height: $spinner-size;
        content: '';
        animation: spin 0.8s linear infinite;
        border: 2px solid currentColor;
        border-right-color: transparent;
        border-radius: 50%;
    }

    &:disabled {
        cursor: not-allowed;
        color: $color-ink-faint;
        border-color: transparent;
        background-color: $color-surface-muted;
        box-shadow: none;
    }

    &--loading:disabled {
        cursor: progress;
    }
}
</style>

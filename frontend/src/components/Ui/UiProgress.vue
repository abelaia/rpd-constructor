<script setup>
defineProps({
    value: {type: Number, required: true},
    label: {type: String, required: true},
    isOnDark: {type: Boolean, default: false},
});
</script>

<template>
    <span
        :class="['ui-progress', {'ui-progress--on-dark': isOnDark}]"
        role="progressbar"
        :aria-valuenow="Math.round(value)"
        aria-valuemin="0"
        aria-valuemax="100"
        :aria-label="label"
    >
        <span
            class="ui-progress__fill"
            :style="{width: `${Math.min(value, 100)}%`}"
        />
    </span>
</template>

<style lang="scss">
$track-height: 6px;

.ui-progress {
    display: block;
    overflow: hidden;
    height: $track-height;
    border-radius: $radius-chip;
    background-color: $color-surface-muted;

    &__fill {
        display: block;
        height: 100%;
        transition: width $duration-slow $ease-out;
        border-radius: inherit;
        background-color: $color-amber;
    }

    &--on-dark {
        background-color: rgba($color-white, 20%);
    }
}
</style>

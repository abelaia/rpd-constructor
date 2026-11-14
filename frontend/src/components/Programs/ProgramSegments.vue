<script setup>
import {computed} from 'vue';
import {CONTENT_SECTIONS} from '@/core/data/sections';

const props = defineProps({
    /** @type {import('vue').PropType<Record<string, string>>} */
    statuses: {type: Object, required: true},
});

const segments = computed(() =>
    CONTENT_SECTIONS.map((section) => ({id: section.id, status: props.statuses[section.id]})),
);
</script>

<template>
    <span
        class="program-segments"
        aria-hidden="true"
    >
        <span
            v-for="segment in segments"
            :key="segment.id"
            :class="['program-segments__item', `program-segments__item--${segment.status}`]"
        />
    </span>
</template>

<style lang="scss">
$segment-height: 8px;

.program-segments {
    display: flex;
    gap: $indent-step * 0.75;

    &__item {
        flex: 1;
        height: $segment-height;
        border-radius: $segment-height * 0.5;
        background-color: $color-line-strong;

        &--done {
            background-color: $color-teal;
        }

        &--in-progress {
            background-color: $color-amber;
        }

        &--error {
            background-color: $color-danger;
        }
    }
}
</style>

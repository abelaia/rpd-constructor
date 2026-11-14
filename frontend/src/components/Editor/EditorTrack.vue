<script setup>
import {computed, onMounted, watch} from 'vue';
import {SECTION_STATUS} from '@/core/constants';
import {SECTIONS} from '@/core/data/sections';

const STATUS_LABELS = Object.freeze({
    [SECTION_STATUS.empty]: 'не заполнен',
    [SECTION_STATUS.inProgress]: 'в работе',
    [SECTION_STATUS.done]: 'заполнен',
    [SECTION_STATUS.error]: 'есть ошибка',
});

const props = defineProps({
    activeId: {type: String, required: true},
    /** @type {import('vue').PropType<Record<string, string>>} */
    statuses: {type: Object, required: true},
});

const emit = defineEmits(['open']);

/** @type {Map<string, HTMLElement>} */
const itemElements = new Map();

const items = computed(() =>
    SECTIONS.map((section) => ({
        ...section,
        status: props.statuses[section.id] ?? SECTION_STATUS.empty,
        isActive: section.id === props.activeId,
    })),
);

watch(() => props.activeId, revealActive, {flush: 'post'});

onMounted(revealActive);

function revealActive() {
    itemElements.get(props.activeId)?.scrollIntoView({block: 'nearest', inline: 'center'});
}

/**
 * @param {string} id
 * @returns {(element: HTMLElement | null) => void}
 */
function setItemElement(id) {
    return (element) => {
        if (element) {
            itemElements.set(id, element);

            return;
        }

        itemElements.delete(id);
    };
}
</script>

<template>
    <nav
        class="editor-track"
        aria-label="Разделы программы"
    >
        <button
            v-for="item in items"
            :key="item.id"
            :ref="setItemElement(item.id)"
            type="button"
            :class="[
                'editor-track__item',
                `editor-track__item--${item.status}`,
                {'editor-track__item--active': item.isActive},
            ]"
            :aria-current="item.isActive ? 'step' : undefined"
            @click="emit('open', item.id)"
        >
            <span class="editor-track__top">
                <span
                    class="editor-track__mark"
                    aria-hidden="true"
                />
                <span class="editor-track__numeral">{{ item.numeral }}</span>
            </span>
            <span class="editor-track__title">{{ item.title }}</span>
            <span class="editor-track__short">{{ item.shortTitle }}</span>
            <span class="editor-track__status">, {{ STATUS_LABELS[item.status] }}</span>
        </button>
    </nav>
</template>

<style lang="scss">
$mark-size: 18px;
$item-min-height: 84px;
$stripe-height: 4px;

.editor-track {
    $block: &;

    display: grid;
    grid-template-columns: repeat(10, minmax(0, 1fr));
    border: 1px solid $color-line;
    border-radius: $radius-card;
    background-color: $color-surface;
    box-shadow: $shadow-card;
    gap: $indent-step * 1.5;

    @include padding('y', 2);
    @include padding('x', 2);

    &__item {
        position: relative;
        display: flex;
        flex-direction: column;
        min-height: $item-min-height;
        text-align: left;
        transition: background-color $duration ease;
        color: $color-ink-soft;
        border: none;
        border-radius: $radius-panel;
        background: transparent;
        font-size: $font-size-xs;
        font-weight: $font-weight-semibold;
        line-height: 1.25;
        gap: $indent-step * 1.5;

        @include padding('top', 3);
        @include padding('x', 2.5);
        @include padding('bottom', 2.5);

        &::before {
            position: absolute;
            top: 0;
            right: $indent-step * 2.5;
            left: $indent-step * 2.5;
            height: $stripe-height;
            content: '';
            border-radius: 0 0 $stripe-height $stripe-height;
            background-color: $color-line-strong;
        }

        @include hover {
            background-color: $color-surface-muted;
        }

        &--done {
            &::before {
                background-color: $color-teal;
            }

            #{$block}__mark {
                border-color: $color-teal;
                background-color: $color-teal;

                &::after {
                    width: 5px;
                    height: 9px;
                    margin-top: -2px;
                    content: '';
                    transform: rotate(45deg);
                    border: solid $color-white;
                    border-width: 0 2px 2px 0;
                }
            }
        }

        &--in-progress {
            &::before {
                background-color: $color-amber;
            }

            #{$block}__mark {
                border-color: $color-amber;

                &::after {
                    width: 8px;
                    height: 8px;
                    content: '';
                    border-radius: 50%;
                    background-color: $color-amber;
                }
            }
        }

        &--error {
            &::before {
                background-color: $color-danger;
            }

            #{$block}__mark {
                border-color: $color-danger;

                &::after {
                    width: 8px;
                    height: 8px;
                    content: '';
                    border-radius: 50%;
                    background-color: $color-danger;
                }
            }
        }

        &--active {
            color: $color-white;
            background-color: $color-pine;
            font-weight: $font-weight-bold;

            @include hover {
                background-color: $color-pine;
            }

            #{$block}__numeral {
                color: $color-white;
            }

            #{$block}__mark {
                border-color: rgba($color-white, 70%);
            }
        }
    }

    &__top {
        display: flex;
        align-items: center;
        gap: $indent-step * 1.5;
    }

    &__mark {
        width: $mark-size;
        height: $mark-size;
        border: 1.5px solid $color-ink-faint;
        border-radius: 50%;

        @include flex-center;
    }

    &__numeral {
        color: $color-ink;
        font-size: $font-size-sm;
        font-weight: $font-weight-extrabold;
        font-variant-numeric: tabular-nums;
    }

    &__short,
    &__status {
        position: absolute;
        overflow: hidden;
        clip: rect(0 0 0 0);
        width: 1px;
        height: 1px;
        white-space: nowrap;
    }

    @include tablet {
        display: flex;
        overflow-x: auto;
        border-radius: $radius-chip;
        gap: $indent-step * 2;

        @include padding('y', 1.5);
        @include padding('x', 1.5);

        &__item {
            flex-direction: row;
            align-items: center;
            flex: none;
            min-height: $control-height-sm + $indent-step;
            border: 1px solid $color-line-strong;
            border-radius: $radius-chip;
            font-size: $font-size-sm;

            @include padding('y', 0);
            @include padding('x', 3.5);

            &::before {
                display: none;
            }
        }

        &__numeral {
            display: none;
        }

        &__title {
            position: absolute;
            overflow: hidden;
            clip: rect(0 0 0 0);
            width: 1px;
            height: 1px;
        }

        &__short {
            position: static;
            overflow: visible;
            clip: auto;
            width: auto;
            height: auto;
        }
    }
}
</style>

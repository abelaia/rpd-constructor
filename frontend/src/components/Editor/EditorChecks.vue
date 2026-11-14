<script setup>
import {computed} from 'vue';
import {CircleAlert, CircleCheck, CircleX} from 'lucide-vue-next';
import {CHECK_LEVELS} from '@/core/constants';

const ICONS = Object.freeze({
    [CHECK_LEVELS.ok]: CircleCheck,
    [CHECK_LEVELS.warning]: CircleAlert,
    [CHECK_LEVELS.error]: CircleX,
});

const props = defineProps({
    /** @type {import('vue').PropType<import('@/core/types/program').ProgramCheck[]>} */
    checks: {type: Array, required: true},
});

const emit = defineEmits(['open']);

const issueCount = computed(() => props.checks.filter((check) => check.level !== CHECK_LEVELS.ok).length);
const summary = computed(() =>
    issueCount.value === 0
        ? 'Все проверки пройдены.'
        : `Замечаний: ${issueCount.value} из ${props.checks.length}. Документ можно скачать и с ними.`,
);
</script>

<template>
    <div class="editor-checks">
        <div class="editor-checks__head">
            <h2 class="editor-checks__title">Перед скачиванием</h2>
            <p class="editor-checks__summary">{{ summary }}</p>
        </div>
        <ul class="editor-checks__list">
            <li
                v-for="check in checks"
                :key="check.id"
                :class="['editor-checks__item', `editor-checks__item--${check.level}`]"
            >
                <component
                    :is="ICONS[check.level]"
                    class="editor-checks__icon"
                    :size="20"
                    aria-hidden="true"
                />
                <span class="editor-checks__text">
                    <b class="editor-checks__item-title">{{ check.title }}</b>
                    <span class="editor-checks__hint">{{ check.hint }}</span>
                    <button
                        type="button"
                        class="editor-checks__link"
                        @click="emit('open', check.sectionId)"
                    >
                        Перейти
                    </button>
                </span>
            </li>
        </ul>
    </div>
</template>

<style lang="scss">
.editor-checks {
    @include column($indent-step * 4);

    &__head {
        @include column($indent-step * 0.5);
    }

    &__title {
        font-size: $font-size-lg;
        font-weight: $font-weight-semibold;
    }

    &__summary {
        @include caption;
    }

    &__list {
        margin: 0;
        padding: 0;
        list-style: none;

        @include column($indent-step * 3);
    }

    &__item {
        display: flex;
        border-radius: $radius-panel;
        gap: $indent-step * 3;

        @include padding('y', 3);
        @include padding('x', 3);

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

    &__icon {
        flex: none;
    }

    &__text {
        flex: 1;
        min-width: 0;

        @include column($indent-step * 0.5);
    }

    &__item-title {
        font-variant-numeric: tabular-nums;
    }

    &__hint {
        font-size: $font-size-sm;
        line-height: 1.4;
    }

    &__link {
        align-self: flex-start;
        margin-top: $indent-step;
        text-decoration: underline;
        color: inherit;
        font-size: $font-size-sm;
        font-weight: $font-weight-bold;

        @include button-reset;
    }
}
</style>

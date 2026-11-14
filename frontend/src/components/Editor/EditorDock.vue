<script setup>
import {computed} from 'vue';
import {ArrowLeft, ArrowRight, Eye} from 'lucide-vue-next';
import {CONTENT_SECTIONS} from '@/core/data/sections';

import UiButton from '@/components/Ui/UiButton.vue';
import UiProgress from '@/components/Ui/UiProgress.vue';

const props = defineProps({
    doneCount: {type: Number, required: true},
    /** @type {import('vue').PropType<import('@/core/types/program').SectionInfo | null>} */
    previousSection: {type: Object, default: null},
    /** @type {import('vue').PropType<import('@/core/types/program').SectionInfo | null>} */
    nextSection: {type: Object, default: null},
    isPreviewButtonVisible: {type: Boolean, default: false},
});

const emit = defineEmits(['previous', 'next', 'finish', 'preview']);

const total = CONTENT_SECTIONS.length;

const percent = computed(() => (props.doneCount / total) * 100);
const nextLabel = computed(() => {
    if (!props.nextSection) {
        return 'Собрать документ';
    }

    return `Далее: ${[props.nextSection.numeral, props.nextSection.title].filter(Boolean).join('. ')}`;
});

function handleNext() {
    emit(props.nextSection ? 'next' : 'finish');
}
</script>

<template>
    <div class="editor-dock">
        <span class="editor-dock__progress">
            <span class="editor-dock__label">{{ doneCount }} из {{ total }} разделов заполнено</span>
            <UiProgress
                :value="percent"
                :label="`Заполнено ${doneCount} разделов из ${total}`"
                is-on-dark
            />
        </span>
        <button
            v-if="isPreviewButtonVisible"
            type="button"
            class="editor-dock__preview"
            aria-label="Открыть предпросмотр и проверки"
            @click="emit('preview')"
        >
            <Eye
                :size="20"
                aria-hidden="true"
            />
        </button>
        <UiButton
            v-if="previousSection"
            theme="inverse"
            class="editor-dock__back"
            @click="emit('previous')"
        >
            <ArrowLeft
                :size="18"
                aria-hidden="true"
            />
            Назад
        </UiButton>
        <UiButton @click="handleNext">
            {{ nextLabel }}
            <ArrowRight
                :size="18"
                aria-hidden="true"
            />
        </UiButton>
    </div>
</template>

<style lang="scss">
$dock-max-width: 920px;
$dock-radius: 32px;

.editor-dock {
    position: sticky;
    z-index: $ui-index-2;
    bottom: $indent-step * 4;
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    width: calc(100% - #{$page-gutter * 2});
    max-width: $dock-max-width;
    margin: ($indent-step * 6) auto ($indent-step * 4);
    color: $color-white;
    border-radius: $dock-radius;
    background-color: $color-pine;
    box-shadow: $shadow-popover;
    gap: ($indent-step * 3) ($indent-step * 4);

    @include padding('y', 2.5);
    @include padding('left', 7);
    @include padding('right', 2.5);

    &__progress {
        flex: 1 1 200px;

        @include column($indent-step * 1.5);
    }

    &__label {
        font-size: $font-size-sm;
        font-weight: $font-weight-semibold;
        font-variant-numeric: tabular-nums;
    }

    &__preview {
        color: $color-white;

        @include icon-button;

        @include hover {
            color: $color-white;
            background-color: rgba($color-white, 14%);
        }

        &:focus-visible {
            outline-color: $color-white;
        }
    }

    @include mobile {
        flex-wrap: nowrap;
        width: calc(100% - #{$indent-step * 4});

        @include padding('left', 2.5);

        &__progress,
        &__back {
            display: none;
        }

        .ui-button {
            flex: 1;
            white-space: normal;
        }
    }
}
</style>

<script setup>
import {ArrowLeft, Check, Download, PencilLine} from 'lucide-vue-next';
import {ROUTE_NAMES} from '@/core/constants';

import UiButton from '@/components/Ui/UiButton.vue';

defineProps({
    /** @type {import('vue').PropType<import('@/core/types/program').Program>} */
    program: {type: Object, required: true},
    savedAtLabel: {type: String, required: true},
    isDownloading: {type: Boolean, default: false},
});

const emit = defineEmits(['rename', 'download']);
</script>

<template>
    <div class="editor-topbar">
        <UiButton
            theme="text"
            size="small"
            :to="{name: ROUTE_NAMES.programs}"
        >
            <ArrowLeft
                :size="16"
                aria-hidden="true"
            />
            Программы
        </UiButton>
        <span
            class="editor-topbar__divider"
            aria-hidden="true"
        />
        <label class="editor-topbar__name">
            <input
                class="editor-topbar__input"
                :value="program.disciplineName"
                aria-label="Название дисциплины"
                @change="emit('rename', $event.target.value)"
            />
            <PencilLine
                class="editor-topbar__pencil"
                :size="16"
                aria-hidden="true"
            />
        </label>
        <span
            v-if="program.code"
            class="editor-topbar__code"
        >
            {{ [program.code, program.semester].filter(Boolean).join(' · ') }}
        </span>
        <span
            class="editor-topbar__saved"
            role="status"
        >
            <Check
                :size="16"
                aria-hidden="true"
            />
            {{ savedAtLabel }}
        </span>
        <UiButton
            theme="outline"
            size="small"
            :is-loading="isDownloading"
            @click="emit('download')"
        >
            <Download
                v-if="!isDownloading"
                :size="16"
                aria-hidden="true"
            />
            Скачать .docx
        </UiButton>
    </div>
</template>

<style lang="scss">
$name-max-width: 420px;

.editor-topbar {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    border: 1px solid $color-line;
    border-radius: $radius-card;
    background-color: $color-surface;
    gap: $indent-step * 3;

    @include padding('y', 2);
    @include padding('x', 4);

    &__divider {
        width: 1px;
        height: $indent-step * 6;
        background-color: $color-line;
    }

    &__name {
        position: relative;
        display: flex;
        align-items: center;
        flex: 0 1 $name-max-width;
        min-width: 0;
    }

    &__input {
        width: 100%;
        transition:
            border-color $duration ease,
            background-color $duration ease;
        color: $color-ink;
        border: 1px solid transparent;
        border-radius: $radius-field;
        background: transparent;
        font: inherit;
        font-size: $font-size-md + 1px;
        font-weight: $font-weight-bold;

        @include padding('y', 1.5);
        @include padding('left', 2.5);
        @include padding('right', 8);

        @include hover {
            background-color: $color-surface-muted;
        }

        &:focus {
            border-color: $color-teal;
            outline: none;
            background-color: $color-surface;
        }
    }

    &__pencil {
        position: absolute;
        right: $indent-step * 2.5;
        pointer-events: none;
        color: $color-ink-soft;
    }

    &__code {
        font-variant-numeric: tabular-nums;

        @include caption;
    }

    &__saved {
        display: inline-flex;
        align-items: center;
        margin-left: auto;
        color: $color-teal;
        gap: $indent-step * 1.5;

        @include caption;
    }

    @include mobile {
        &__divider,
        &__code {
            display: none;
        }

        &__name {
            flex-basis: 100%;
            order: 1;
        }
    }
}
</style>

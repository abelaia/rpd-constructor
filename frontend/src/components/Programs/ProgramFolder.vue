<script setup>
import {computed} from 'vue';
import {
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuPortal,
    DropdownMenuRoot,
    DropdownMenuTrigger,
} from 'reka-ui';
import {Copy, Download, Ellipsis, FileText, Trash2} from 'lucide-vue-next';
import {ROUTE_NAMES} from '@/core/constants';
import {CONTENT_SECTIONS} from '@/core/data/sections';
import {formatChangedAt} from '@/core/utils/format';
import {getDoneCount, getSectionStatuses, isProgramDone} from '@/core/utils/programs';

import ProgramSegments from '@/components/Programs/ProgramSegments.vue';
import UiButton from '@/components/Ui/UiButton.vue';

const props = defineProps({
    /** @type {import('vue').PropType<import('@/core/types/program').Program>} */
    program: {type: Object, required: true},
    isDownloading: {type: Boolean, default: false},
});

const emit = defineEmits(['download', 'duplicate', 'remove']);

const isDone = computed(() => isProgramDone(props.program));
const statuses = computed(() => getSectionStatuses(props.program));
const doneLabel = computed(() => `${getDoneCount(props.program)} из ${CONTENT_SECTIONS.length}`);
const tabLabel = computed(() => [isDone.value ? 'Готова' : 'В работе', props.program.code].filter(Boolean).join(' · '));
const details = computed(() => [props.program.semester, props.program.teacherName].filter(Boolean).join(' · '));
const changedLabel = computed(() => `изменена ${formatChangedAt(props.program.changedAt)}`);
const editorRoute = computed(() => ({name: ROUTE_NAMES.editor, params: {id: props.program.id}}));
</script>

<template>
    <article class="program-folder">
        <span :class="['program-folder__tab', {'program-folder__tab--done': isDone}]">{{ tabLabel }}</span>
        <div class="program-folder__head">
            <div class="program-folder__names">
                <h3 class="program-folder__title">{{ program.disciplineName }}</h3>
                <span
                    v-if="details"
                    class="program-folder__details"
                >
                    {{ details }}
                </span>
            </div>
            <span
                class="program-folder__icon"
                aria-hidden="true"
            >
                <FileText :size="24" />
            </span>
        </div>
        <div class="program-folder__progress">
            <ProgramSegments :statuses="statuses" />
            <div class="program-folder__meta">
                <span>
                    <b class="program-folder__done">{{ doneLabel }}</b>
                    разделов
                </span>
                <span>{{ changedLabel }}</span>
            </div>
        </div>
        <div class="program-folder__actions">
            <UiButton
                theme="secondary"
                size="small"
                :to="editorRoute"
            >
                Открыть
            </UiButton>
            <UiButton
                theme="text"
                size="small"
                :is-loading="isDownloading"
                @click="emit('download', program)"
            >
                <Download
                    v-if="!isDownloading"
                    :size="16"
                    aria-hidden="true"
                />
                Скачать .docx
            </UiButton>
            <DropdownMenuRoot>
                <DropdownMenuTrigger
                    class="program-folder__more"
                    aria-label="Ещё действия"
                >
                    <Ellipsis
                        :size="20"
                        aria-hidden="true"
                    />
                </DropdownMenuTrigger>
                <DropdownMenuPortal>
                    <DropdownMenuContent
                        class="program-folder-menu"
                        align="end"
                        :side-offset="4"
                    >
                        <DropdownMenuItem
                            class="program-folder-menu__item"
                            @select="emit('duplicate', program)"
                        >
                            <Copy
                                :size="16"
                                aria-hidden="true"
                            />
                            Дублировать
                        </DropdownMenuItem>
                        <DropdownMenuItem
                            class="program-folder-menu__item program-folder-menu__item--danger"
                            @select="emit('remove', program)"
                        >
                            <Trash2
                                :size="16"
                                aria-hidden="true"
                            />
                            Удалить
                        </DropdownMenuItem>
                    </DropdownMenuContent>
                </DropdownMenuPortal>
            </DropdownMenuRoot>
        </div>
    </article>
</template>

<style lang="scss">
$tab-height: 28px;
$icon-size: 48px;
$menu-width: 200px;

.program-folder {
    position: relative;
    margin-top: $tab-height;
    border: 1px solid $color-line;
    border-radius: 0 $radius-card $radius-card $radius-card;
    background-color: $color-surface;
    box-shadow: $shadow-card;

    @include lift;
    @include column($indent-step * 4);
    @include padding('top', 6);
    @include padding('x', 5);
    @include padding('bottom', 3);

    &__tab {
        position: absolute;
        top: -$tab-height;
        left: -1px;
        display: inline-flex;
        align-items: center;
        height: $tab-height;
        color: $color-honey-ink;
        border: 1px solid rgba($color-amber, 45%);
        border-bottom: none;
        border-radius: $radius-panel $radius-panel 0 0;
        background-color: $color-honey;
        font-size: $font-size-xs;
        font-weight: $font-weight-bold;
        font-variant-numeric: tabular-nums;
        gap: $indent-step * 2;

        @include padding('x', 4);

        &::before {
            width: 6px;
            height: 6px;
            content: '';
            border-radius: 50%;
            background-color: currentColor;
        }

        &--done {
            color: $color-teal;
            border-color: $color-mint-line;
            background-color: $color-mint;
        }
    }

    &__head {
        display: flex;
        align-items: flex-start;
        gap: $indent-step * 3.5;
    }

    &__names {
        flex: 1;
        min-width: 0;

        @include column($indent-step);
    }

    &__title {
        overflow-wrap: anywhere;

        @include display($font-size-lg + 2px);
    }

    &__details {
        @include caption;
    }

    &__icon {
        flex: none;
        width: $icon-size;
        height: $icon-size;
        color: $color-teal;
        border-radius: $radius-panel;
        background-color: $color-mint;

        @include flex-center;
    }

    &__progress {
        @include column($indent-step * 2);
    }

    &__meta {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        font-variant-numeric: tabular-nums;
        gap: $indent-step ($indent-step * 3);

        @include caption;
    }

    &__done {
        color: $color-ink;
    }

    &__actions {
        display: flex;
        align-items: center;
        border-top: 1px dashed $color-line-strong;
        gap: $indent-step * 2;

        @include padding('top', 2);
    }

    &__more {
        margin-left: auto;

        @include icon-button;
    }
}

.program-folder-menu {
    z-index: $ui-index-2;
    width: $menu-width;
    border: 1px solid $color-line;
    border-radius: $radius-panel;
    background-color: $color-surface;
    box-shadow: $shadow-popover;

    @include column($indent-step * 0.5);
    @include padding('y', 1.5);
    @include padding('x', 1.5);

    &__item {
        display: flex;
        align-items: center;
        min-height: $control-height-sm + $indent-step;
        cursor: pointer;
        border-radius: $indent-step * 2;
        outline: none;
        font-size: $font-size-sm + 1px;
        gap: $indent-step * 2.5;

        @include padding('x', 2.5);

        &[data-highlighted] {
            background-color: $color-surface-muted;
        }

        &--danger {
            color: $color-danger;
        }
    }
}
</style>

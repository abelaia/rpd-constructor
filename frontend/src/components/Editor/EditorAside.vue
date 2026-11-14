<script setup>
import {computed} from 'vue';
import {TabsContent, TabsList, TabsRoot, TabsTrigger} from 'reka-ui';
import {CHECK_LEVELS} from '@/core/constants';
import {getChecks} from '@/core/utils/programs';

import EditorChecks from '@/components/Editor/EditorChecks.vue';
import EditorPreview from '@/components/Editor/EditorPreview.vue';

const TABS = Object.freeze({preview: 'preview', checks: 'checks'});

const props = defineProps({
    /** @type {import('vue').PropType<import('@/core/types/program').Program>} */
    program: {type: Object, required: true},
    /** @type {import('vue').PropType<import('@/core/types/program').SectionInfo>} */
    section: {type: Object, required: true},
});

const emit = defineEmits(['open']);

const checks = computed(() => getChecks(props.program));
const issueCount = computed(() => checks.value.filter((check) => check.level !== CHECK_LEVELS.ok).length);
</script>

<template>
    <TabsRoot
        class="editor-aside"
        :default-value="TABS.preview"
    >
        <TabsList
            class="editor-aside__tabs"
            aria-label="Предпросмотр и проверки"
        >
            <TabsTrigger
                class="editor-aside__tab"
                :value="TABS.preview"
            >
                Предпросмотр
            </TabsTrigger>
            <TabsTrigger
                class="editor-aside__tab"
                :value="TABS.checks"
            >
                Проверки
                <span
                    v-if="issueCount > 0"
                    class="editor-aside__badge"
                    :aria-label="`замечаний: ${issueCount}`"
                >
                    {{ issueCount }}
                </span>
            </TabsTrigger>
        </TabsList>
        <TabsContent
            class="editor-aside__panel"
            :value="TABS.preview"
        >
            <EditorPreview
                :program="program"
                :section="section"
            />
        </TabsContent>
        <TabsContent
            class="editor-aside__panel editor-aside__panel--card"
            :value="TABS.checks"
        >
            <EditorChecks
                :checks="checks"
                @open="emit('open', $event)"
            />
        </TabsContent>
    </TabsRoot>
</template>

<style lang="scss">
$badge-size: 18px;

.editor-aside {
    @include column($indent-step * 4);

    &__tabs {
        display: flex;
        border-radius: $radius-chip;
        background-color: $color-surface-muted;
        gap: $indent-step;

        @include padding('y', 1);
        @include padding('x', 1);
    }

    &__tab {
        display: inline-flex;
        align-items: center;
        flex: 1;
        justify-content: center;
        height: $control-height-sm;
        color: $color-ink-soft;
        border: none;
        border-radius: $radius-chip;
        background: transparent;
        font-size: $font-size-sm;
        font-weight: $font-weight-semibold;
        gap: $indent-step * 1.5;

        &[data-state='active'] {
            color: $color-ink;
            background-color: $color-surface;
            box-shadow: 0 1px 3px rgba($color-ink, 18%);
            font-weight: $font-weight-bold;
        }
    }

    &__badge {
        min-width: $badge-size;
        height: $badge-size;
        color: $color-white;
        border-radius: $radius-chip;
        background-color: $color-danger;
        font-size: $font-size-xs - 1px;
        font-weight: $font-weight-bold;

        @include flex-center;
        @include padding('x', 1.25);
    }

    &__panel {
        outline: none;

        &--card {
            @include card;
            @include padding('y', 5);
            @include padding('x', 5);
        }
    }
}
</style>

<script setup>
import {computed, ref} from 'vue';
import {useRouter} from 'vue-router';
import {
    BookOpen,
    ClipboardCheck,
    Compass,
    FileBadge,
    LayoutList,
    Medal,
    MonitorPlay,
    Puzzle,
    ScrollText,
    Target,
} from 'lucide-vue-next';
import {ROUTE_NAMES, SECTION_KINDS, TITLE_SECTION_ID} from '@/core/constants';
import {useDownloadProgram} from '@/composables/useDownloadProgram';
import {useProgramEditor} from '@/composables/useProgramEditor';

import EditorAside from '@/components/Editor/EditorAside.vue';
import EditorDock from '@/components/Editor/EditorDock.vue';
import EditorTopbar from '@/components/Editor/EditorTopbar.vue';
import EditorTrack from '@/components/Editor/EditorTrack.vue';
import SectionAssessment from '@/components/Editor/SectionAssessment.vue';
import SectionCompetencies from '@/components/Editor/SectionCompetencies.vue';
import SectionContent from '@/components/Editor/SectionContent.vue';
import SectionEquipment from '@/components/Editor/SectionEquipment.vue';
import SectionLiterature from '@/components/Editor/SectionLiterature.vue';
import SectionText from '@/components/Editor/SectionText.vue';
import SectionTitle from '@/components/Editor/SectionTitle.vue';
import UiButton from '@/components/Ui/UiButton.vue';
import UiModal from '@/components/Ui/UiModal.vue';

const SECTION_COMPONENTS = Object.freeze({
    [SECTION_KINDS.title]: SectionTitle,
    [SECTION_KINDS.text]: SectionText,
    [SECTION_KINDS.competencies]: SectionCompetencies,
    [SECTION_KINDS.content]: SectionContent,
    [SECTION_KINDS.literature]: SectionLiterature,
    [SECTION_KINDS.equipment]: SectionEquipment,
    [SECTION_KINDS.assessment]: SectionAssessment,
});

const SECTION_ICONS = Object.freeze({
    [TITLE_SECTION_ID]: FileBadge,
    I: Target,
    II: Puzzle,
    III: Medal,
    IV: LayoutList,
    V: BookOpen,
    VI: MonitorPlay,
    VII: Compass,
    VIII: ClipboardCheck,
    IX: ScrollText,
});

const router = useRouter();
const {
    program,
    activeSection,
    previousSection,
    nextSection,
    statuses,
    doneCount,
    savedAtLabel,
    update,
    updateSections,
    openSection,
} = useProgramEditor();
const {isDownloading, download} = useDownloadProgram();

const isSheetOpen = ref(false);

const isWideSection = computed(() => activeSection.value.kind === SECTION_KINDS.content);
const sectionHeading = computed(() =>
    [activeSection.value.numeral, activeSection.value.title].filter(Boolean).join('. '),
);

/** @param {string} name */
function handleRename(name) {
    if (name.trim() !== '') {
        update({disciplineName: name.trim()});
    }
}

function handleDownload() {
    download(program.value);
}

function handlePrevious() {
    openSection(previousSection.value.id);
}

function handleNext() {
    openSection(nextSection.value.id);
}

function handleFinish() {
    router.push({name: ROUTE_NAMES.ready, params: {id: program.value.id}});
}

/** @param {string} sectionId */
function handleCheckOpen(sectionId) {
    isSheetOpen.value = false;
    openSection(sectionId);
}

function handleSheetOpen() {
    isSheetOpen.value = true;
}

function handleSheetClose() {
    isSheetOpen.value = false;
}
</script>

<template>
    <div
        v-if="program"
        class="editor-page"
    >
        <div class="editor-page__head">
            <EditorTopbar
                :program="program"
                :saved-at-label="savedAtLabel"
                :is-downloading="isDownloading"
                @rename="handleRename"
                @download="handleDownload"
            />
            <EditorTrack
                :active-id="activeSection.id"
                :statuses="statuses"
                @open="openSection"
            />
        </div>
        <div :class="['editor-page__body', {'editor-page__body--wide': isWideSection}]">
            <section
                class="editor-page__panel"
                :aria-labelledby="`section-${activeSection.id}`"
            >
                <header class="editor-page__intro">
                    <span
                        class="editor-page__icon"
                        aria-hidden="true"
                    >
                        <component
                            :is="SECTION_ICONS[activeSection.id]"
                            :size="36"
                        />
                    </span>
                    <div class="editor-page__intro-text">
                        <h1
                            :id="`section-${activeSection.id}`"
                            class="editor-page__title"
                        >
                            {{ sectionHeading }}
                        </h1>
                        <p class="editor-page__hint">{{ activeSection.hint }}</p>
                    </div>
                </header>
                <component
                    :is="SECTION_COMPONENTS[activeSection.kind]"
                    :key="activeSection.id"
                    :program="program"
                    :section="activeSection"
                    @update="update"
                    @update-sections="updateSections"
                />
            </section>
            <EditorAside
                v-if="!isWideSection"
                class="editor-page__aside"
                :program="program"
                :section="activeSection"
                @open="handleCheckOpen"
            />
        </div>
        <EditorDock
            :done-count="doneCount"
            :previous-section="previousSection"
            :next-section="nextSection"
            :is-preview-button-visible="isWideSection"
            @previous="handlePrevious"
            @next="handleNext"
            @finish="handleFinish"
            @preview="handleSheetOpen"
        />
        <button
            type="button"
            class="editor-page__sheet-button"
            @click="handleSheetOpen"
        >
            Предпросмотр и проверки
        </button>
        <UiModal
            v-if="isSheetOpen"
            title="Предпросмотр"
            is-sheet
            @close="handleSheetClose"
        >
            <EditorAside
                :program="program"
                :section="activeSection"
                @open="handleCheckOpen"
            />
        </UiModal>
    </div>
    <section
        v-else
        class="editor-page__missing"
    >
        <h1 class="editor-page__title">Программа не найдена</h1>
        <p class="editor-page__hint">Возможно, её удалили или ссылка неполная.</p>
        <UiButton :to="{name: ROUTE_NAMES.programs}">К списку программ</UiButton>
    </section>
</template>

<style lang="scss">
$aside-width: 360px;
$icon-size: 72px;

.editor-page {
    @include padding('top', 3);

    &__head {
        @include column($indent-step * 3);
        @include padding('x', 6);
    }

    &__body {
        display: flex;
        align-items: flex-start;
        gap: $indent-step * 6;

        @include padding('top', 6);
        @include padding('x', 6);
    }

    &__panel {
        flex: 1;
        min-width: 0;

        @include card;
        @include column($indent-step * 6);
        @include padding('y', 6);
        @include padding('x', 6);
    }

    &__intro {
        display: flex;
        align-items: center;
        gap: $indent-step * 5;
    }

    &__icon {
        flex: none;
        width: $icon-size;
        height: $icon-size;
        color: $color-teal;
        border-radius: $radius-tile + 4px;
        background-color: $color-mint;

        @include flex-center;
    }

    &__intro-text {
        flex: 1;
        min-width: 0;

        @include column($indent-step * 1.5);
    }

    &__title {
        @include display($font-size-xxl);
    }

    &__hint {
        max-width: 680px;
        color: $color-ink-soft;
    }

    &__aside {
        position: sticky;
        top: $indent-step * 4;
        flex: none;
        width: $aside-width;
    }

    &__sheet-button {
        display: none;
    }

    &__missing {
        align-items: flex-start;

        @include column($indent-step * 4);
        @include padding('y', 12);
        @include padding('x', 6);
    }

    @include tablet {
        &__body {
            flex-direction: column;
            align-items: stretch;
        }

        &__aside {
            display: none;
        }

        &__sheet-button {
            display: block;
            margin: 0 auto ($indent-step * 6);
            text-decoration: underline;
            color: $color-teal;
            font-weight: $font-weight-bold;

            @include button-reset;
        }
    }

    @include mobile {
        &__head,
        &__body {
            @include padding('x', 2);
        }

        &__panel {
            @include padding('y', 5);
            @include padding('x', 4);
        }

        &__icon {
            display: none;
        }

        &__title {
            font-size: $font-size-xl + 2px;
        }
    }
}
</style>

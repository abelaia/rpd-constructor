<script setup>
import {computed} from 'vue';
import {useRoute, useRouter} from 'vue-router';
import {ArrowLeft, Download} from 'lucide-vue-next';
import {MAX_POINTS, ROUTE_NAMES} from '@/core/constants';
import {CONTENT_SECTIONS} from '@/core/data/sections';
import {useProgramsStore} from '@/core/stores/programs';
import {useDownloadProgram} from '@/composables/useDownloadProgram';
import {formatChangedAt} from '@/core/utils/format';
import {getChecks, getDoneCount, getHoursTotals, getPointsTotal} from '@/core/utils/programs';

import EditorChecks from '@/components/Editor/EditorChecks.vue';
import UiButton from '@/components/Ui/UiButton.vue';

import checkUrl from '@/assets/images/sticker-check.webp';

const route = useRoute();
const router = useRouter();
const programsStore = useProgramsStore();
const {isDownloading, downloadedFilename, download} = useDownloadProgram();

const program = computed(() => programsStore.getProgram(String(route.params.id)));
const doneCount = computed(() => getDoneCount(program.value));
const isComplete = computed(() => doneCount.value === CONTENT_SECTIONS.length);
const checks = computed(() => getChecks(program.value));
const stats = computed(() => [
    {id: 'sections', value: `${doneCount.value}/${CONTENT_SECTIONS.length}`, label: 'разделов заполнено'},
    {id: 'topics', value: program.value.sections.topics.length, label: 'тем в программе'},
    {id: 'hours', value: getHoursTotals(program.value.sections.topics).total, label: 'часов по темам'},
    {id: 'points', value: `${getPointsTotal(program.value.sections.topics)}/${MAX_POINTS}`, label: 'баллов'},
]);
const editorRoute = computed(() => ({name: ROUTE_NAMES.editor, params: {id: program.value.id}}));
const changedLabel = computed(() => `изменена ${formatChangedAt(program.value.changedAt)}`);

function handleDownload() {
    download(program.value);
}

/** @param {string} sectionId */
function handleCheckOpen(sectionId) {
    router.push({name: ROUTE_NAMES.editor, params: {id: program.value.id, section: sectionId}});
}
</script>

<template>
    <div
        v-if="program"
        class="ready-page"
    >
        <section class="ready-page__hero">
            <img
                class="ready-page__sticker"
                :src="checkUrl"
                alt=""
            />
            <span class="ready-page__bubble">
                {{ isComplete ? 'Все 9 разделов заполнены' : `Заполнено ${doneCount} из 9 разделов` }}
            </span>
            <h1 class="ready-page__title">
                Документ
                <span class="ready-page__highlight">{{ downloadedFilename ? 'скачан' : 'готов' }}</span>
            </h1>
            <p class="ready-page__name">{{ program.disciplineName }}</p>
            <p class="ready-page__meta">
                {{ downloadedFilename ? `${downloadedFilename} · Word` : `Word-документ · ${changedLabel}` }}
            </p>
            <div class="ready-page__actions">
                <UiButton
                    size="large"
                    :is-loading="isDownloading"
                    @click="handleDownload"
                >
                    <Download
                        v-if="!isDownloading"
                        :size="20"
                        aria-hidden="true"
                    />
                    Скачать .docx
                </UiButton>
                <UiButton
                    theme="inverse"
                    size="large"
                    :to="editorRoute"
                >
                    Вернуться к редактированию
                </UiButton>
            </div>
        </section>
        <div class="ready-page__side">
            <dl class="ready-page__stats">
                <div
                    v-for="stat in stats"
                    :key="stat.id"
                    class="ready-page__stat"
                >
                    <dt class="ready-page__stat-label">{{ stat.label }}</dt>
                    <dd class="ready-page__stat-value">{{ stat.value }}</dd>
                </div>
            </dl>
            <div class="ready-page__checks">
                <EditorChecks
                    :checks="checks"
                    @open="handleCheckOpen"
                />
            </div>
            <UiButton
                theme="text"
                class="ready-page__back"
                :to="{name: ROUTE_NAMES.programs}"
            >
                <ArrowLeft
                    :size="18"
                    aria-hidden="true"
                />
                К списку программ
            </UiButton>
        </div>
    </div>
    <section
        v-else
        class="ready-page__missing"
    >
        <h1 class="ready-page__name">Программа не найдена</h1>
        <UiButton :to="{name: ROUTE_NAMES.programs}">К списку программ</UiButton>
    </section>
</template>

<style lang="scss">
$hero-max-width: 520px;
$sticker-size: 140px;
$bubble-radius: 18px;

.ready-page {
    display: flex;
    align-items: flex-start;
    flex-wrap: wrap;
    gap: $indent-step * 6;

    @include padding('y', 6);
    @include padding('x', 6);

    &__hero {
        position: relative;
        flex: 1 1 380px;
        max-width: $hero-max-width;
        color: $color-white;
        border-radius: $radius-hero;
        background-color: $color-pine;

        @include column($indent-step * 4);
        @include padding('y', 10);
        @include padding('x', 10);
    }

    &__sticker {
        width: $sticker-size;
        transform: rotate(-8deg);
    }

    &__bubble {
        align-self: flex-start;
        color: $color-pine;
        border-radius: $bubble-radius $bubble-radius $bubble-radius $indent-step;
        background-color: $color-mint;
        font-weight: $font-weight-bold;

        @include padding('y', 2);
        @include padding('x', 4);
    }

    &__title {
        letter-spacing: -0.03em;
        font-size: 52px;
        font-weight: $font-weight-extrabold;
        line-height: 1.2;
    }

    &__highlight {
        @include highlight-pill;
    }

    &__name {
        overflow-wrap: anywhere;

        @include display($font-size-xl);
    }

    &__meta {
        color: rgba($color-white, 82%);
        font-size: $font-size-sm + 1px;
        font-variant-numeric: tabular-nums;
    }

    &__actions {
        margin-top: $indent-step * 4;

        @include column($indent-step * 3);
    }

    &__side {
        flex: 999 1 420px;
        min-width: 0;

        @include column($indent-step * 6);
    }

    &__stats {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        margin: 0;

        @include card;
        @include padding('y', 6);
        @include padding('x', 2);
    }

    &__stat {
        display: flex;
        flex-direction: column-reverse;
        gap: $indent-step * 0.5;

        @include padding('x', 6);
    }

    &__stat-label {
        @include caption;
    }

    &__stat-value {
        margin: 0;
        letter-spacing: -0.02em;
        font-size: $font-size-xxl;
        font-weight: $font-weight-extrabold;
        line-height: 1.1;
        font-variant-numeric: tabular-nums;
    }

    &__checks {
        @include card;
        @include padding('y', 5);
        @include padding('x', 5);
    }

    &__back {
        align-self: flex-start;
    }

    &__missing {
        align-items: flex-start;

        @include column($indent-step * 4);
        @include padding('y', 12);
        @include padding('x', 6);
    }

    @include mobile {
        @include padding('x', 2);

        &__hero {
            @include padding('y', 7);
            @include padding('x', 5);
        }

        &__title {
            font-size: $font-size-hero - 4px;
        }
    }
}
</style>

<script setup>
import {computed} from 'vue';
import {ArrowRight, MousePointer2, Plus} from 'lucide-vue-next';
import {CONTENT_SECTIONS} from '@/core/data/sections';
import {formatTime, getGreeting} from '@/core/utils/format';
import {getDoneCount} from '@/core/utils/programs';

import UiButton from '@/components/Ui/UiButton.vue';

import bookUrl from '@/assets/images/book.webp';
import heroArtUrl from '@/assets/images/hero-art.webp';
import clipUrl from '@/assets/images/sticker-clip.webp';
import sparkUrl from '@/assets/images/sticker-spark.webp';

const FLOW_STEPS = Object.freeze([
    {id: 'name', label: 'Назвать дисциплину', theme: 'mint'},
    {id: 'fill', label: 'Заполнить 9 разделов', theme: 'honey'},
    {id: 'check', label: 'Проверить суммы', theme: 'teal'},
    {id: 'download', label: 'Скачать Word', theme: 'white'},
]);

const props = defineProps({
    /** @type {import('vue').PropType<import('@/core/types/program').Program | null>} */
    latestProgram: {type: Object, default: null},
    hasPrograms: {type: Boolean, default: false},
});

const emit = defineEmits(['create', 'copy']);

const greeting = computed(() => getGreeting(new Date().getHours()));
const doneLabel = computed(() =>
    props.latestProgram ? `${getDoneCount(props.latestProgram)} из ${CONTENT_SECTIONS.length}` : '',
);
const savedLabel = computed(() =>
    props.latestProgram ? `сохранено в ${formatTime(props.latestProgram.changedAt)}` : '',
);
</script>

<template>
    <section class="programs-hero">
        <div class="programs-hero__text">
            <span class="programs-hero__greeting">{{ greeting }}</span>
            <h1 class="programs-hero__title">
                Рабочая программа — без ручного
                <span class="programs-hero__highlight">форматирования</span>
            </h1>
            <ol
                class="programs-hero__flow"
                aria-label="Как это работает"
            >
                <li
                    v-for="(step, index) in FLOW_STEPS"
                    :key="step.id"
                    class="programs-hero__step"
                >
                    <ArrowRight
                        v-if="index > 0"
                        :size="16"
                        aria-hidden="true"
                    />
                    <span :class="['programs-hero__step-label', `programs-hero__step-label--${step.theme}`]">
                        {{ step.label }}
                    </span>
                </li>
            </ol>
            <div class="programs-hero__actions">
                <UiButton
                    size="large"
                    @click="emit('create')"
                >
                    <Plus
                        :size="20"
                        aria-hidden="true"
                    />
                    Создать программу
                </UiButton>
                <UiButton
                    v-if="hasPrograms"
                    theme="inverse"
                    size="large"
                    @click="emit('copy')"
                >
                    Из существующей
                </UiButton>
            </div>
        </div>
        <div
            class="programs-hero__art"
            aria-hidden="true"
        >
            <img
                class="programs-hero__backdrop"
                :src="heroArtUrl"
                alt=""
            />
            <img
                class="programs-hero__book"
                :src="bookUrl"
                alt=""
            />
            <img
                class="programs-hero__spark"
                :src="sparkUrl"
                alt=""
            />
            <template v-if="latestProgram">
                <div class="programs-hero__sheet">
                    <span>РАБОЧАЯ ПРОГРАММА ДИСЦИПЛИНЫ</span>
                    <span class="programs-hero__sheet-name">{{ latestProgram.disciplineName }}</span>
                    <img
                        class="programs-hero__clip"
                        :src="clipUrl"
                        alt=""
                    />
                </div>
                <span class="programs-hero__sticker">
                    <span class="programs-hero__sticker-value">{{ doneLabel }}</span>
                    разделов
                </span>
                <span class="programs-hero__cursor">
                    <MousePointer2 :size="20" />
                    <span class="programs-hero__cursor-label">{{ savedLabel }}</span>
                </span>
            </template>
        </div>
    </section>
</template>

<style lang="scss">
$art-width: 460px;
$art-height: 420px;
$sheet-width: 168px;
$sheet-height: 216px;
$sticker-size: 104px;
$bubble-radius: 18px;

.programs-hero {
    $block: &;

    position: relative;
    display: flex;
    overflow: hidden;
    align-items: center;
    flex-wrap: wrap;
    color: $color-white;
    border-radius: $radius-hero;
    background-color: $color-pine;
    gap: $indent-step * 8;

    @include padding('y', 14);
    @include padding('left', 14);
    @include padding('right', 10);

    &__text {
        position: relative;
        flex: 1 1 520px;
        min-width: 0;

        @include column($indent-step * 6);
    }

    &__greeting {
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
        font-size: $font-size-display;
        font-weight: $font-weight-extrabold;
        line-height: 1.1;
    }

    &__highlight {
        @include highlight-pill;
    }

    &__flow {
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        margin: 0;
        padding: 0;
        list-style: none;
        gap: $indent-step * 2;
    }

    &__step {
        display: flex;
        align-items: center;
        gap: $indent-step * 2;
    }

    &__step-label {
        display: inline-flex;
        align-items: center;
        height: $control-height-sm;
        border-radius: $radius-chip;
        font-size: $font-size-sm + 1px;
        font-weight: $font-weight-bold;

        @include padding('x', 4);

        &--mint {
            color: $color-pine;
            background-color: $color-mint;
        }

        &--honey {
            color: $color-honey-ink;
            background-color: $color-honey;
        }

        &--teal {
            color: $color-white;
            background-color: $color-teal-light;
        }

        &--white {
            color: $color-ink;
            background-color: $color-white;
        }
    }

    &__actions {
        display: flex;
        flex-wrap: wrap;
        gap: $indent-step * 3;
    }

    &__art {
        position: relative;
        flex: 0 1 $art-width;
        height: $art-height;
    }

    &__backdrop {
        position: absolute;
        top: -($indent-step * 2);
        right: -($indent-step * 17);
        width: 560px;
        height: $art-height;
        opacity: 0.55;
        object-fit: contain;
    }

    &__book {
        position: absolute;
        top: 0;
        left: $indent-step * 12;
        width: 380px;
        height: $art-height;
        object-fit: contain;
    }

    &__spark {
        position: absolute;
        top: -($indent-step * 2);
        left: $indent-step;
        width: 84px;
    }

    &__sheet {
        position: absolute;
        bottom: $indent-step * 2;
        left: 0;
        justify-content: center;
        width: $sheet-width;
        height: $sheet-height;
        transform: rotate(-6deg);
        text-align: center;
        font-size: 9px;
        line-height: 13px;

        @include paper;
        @include column($indent-step * 2);
        @include padding('x', 3);
    }

    &__sheet-name {
        font-size: $font-size-xs;
        font-weight: $font-weight-bold;
        line-height: 1.3;
    }

    &__clip {
        position: absolute;
        top: -($indent-step * 7);
        right: $indent-step * 2;
        width: 40px;
        transform: rotate(14deg);
    }

    &__sticker {
        position: absolute;
        top: $indent-step * 2;
        right: $indent-step * 2;
        flex-direction: column;
        width: $sticker-size;
        height: $sticker-size;
        transform: rotate(10deg);
        color: $color-button-ink;
        border-radius: 50%;
        background-color: $color-amber;
        box-shadow: 0 4px 0 $color-amber-edge;
        font-size: $font-size-sm;
        font-weight: $font-weight-extrabold;
        line-height: 1.05;

        @include flex-center;
    }

    &__sticker-value {
        font-size: 30px;
        font-variant-numeric: tabular-nums;
    }

    &__cursor {
        position: absolute;
        right: $indent-step * 6;
        bottom: $indent-step * 10;
        display: flex;
        align-items: flex-start;
        color: $color-mint;
    }

    &__cursor-label {
        margin-top: $indent-step * 3;
        color: $color-pine;
        border-radius: $indent-step ($indent-step * 3) ($indent-step * 3) ($indent-step * 3);
        background-color: $color-mint;
        font-size: $font-size-xs;
        font-weight: $font-weight-bold;

        @include padding('y', 1);
        @include padding('x', 2.5);
    }

    @include tablet {
        @include padding('y', 8);
        @include padding('x', 6);

        &__title {
            font-size: $font-size-hero;
        }

        &__art {
            display: none;
        }
    }

    @include mobile {
        border-radius: $radius-card;

        &__title {
            font-size: $font-size-xxl - 4px;
        }

        &__highlight {
            border-radius: $radius-panel;

            @include padding('x', 2.5);
        }

        &__actions {
            flex-direction: column;
        }
    }
}
</style>

<script setup>
import {Plus} from 'lucide-vue-next';

import UiButton from '@/components/Ui/UiButton.vue';

import arrowUrl from '@/assets/images/sticker-arrow.webp';
import sheetUrl from '@/assets/images/sticker-sheet.webp';

defineProps({
    isFiltered: {type: Boolean, default: false},
});

const emit = defineEmits(['create']);
</script>

<template>
    <section class="programs-empty">
        <img
            class="programs-empty__art"
            :src="sheetUrl"
            alt=""
        />
        <h2 class="programs-empty__title">
            <template v-if="isFiltered">Ничего не нашлось</template>
            <template v-else>
                Здесь появятся ваши
                <span class="programs-empty__highlight">программы</span>
            </template>
        </h2>
        <p class="programs-empty__text">
            <template v-if="isFiltered">Попробуйте другой запрос или переключите фильтр.</template>
            <template v-else>
                Пока список пуст. Первая программа займёт это место — с дорожкой из девяти разделов и статусом.
            </template>
        </p>
        <template v-if="!isFiltered">
            <img
                class="programs-empty__arrow"
                :src="arrowUrl"
                alt=""
            />
            <UiButton
                size="large"
                @click="emit('create')"
            >
                <Plus
                    :size="20"
                    aria-hidden="true"
                />
                Создать первую программу
            </UiButton>
        </template>
    </section>
</template>

<style lang="scss">
$art-size: 140px;
$text-width: 440px;

.programs-empty {
    align-items: center;
    text-align: center;
    border: 1.5px dashed $color-ink-faint;
    border-radius: $radius-card;

    @include column($indent-step * 3);
    @include padding('y', 12);
    @include padding('x', 6);

    &__art {
        width: $art-size;
        transform: rotate(-6deg);
    }

    &__title {
        @include display($font-size-hero);
    }

    &__highlight {
        @include highlight-pill;
    }

    &__text {
        max-width: $text-width;
        color: $color-ink-soft;
    }

    &__arrow {
        width: 96px;
        margin-left: $indent-step * 40;
        transform: rotate(72deg);
    }

    @include mobile {
        &__title {
            font-size: $font-size-xl + 4px;
        }

        &__arrow {
            display: none;
        }
    }
}
</style>

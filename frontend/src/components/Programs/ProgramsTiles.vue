<script setup>
import {computed} from 'vue';
import {FileCheck2, FilePen, Files} from 'lucide-vue-next';
import {PROGRAM_FILTERS} from '@/core/constants';

const TILES = Object.freeze([
    {filter: PROGRAM_FILTERS.all, label: 'все программы', theme: 'white', icon: Files},
    {filter: PROGRAM_FILTERS.inProgress, label: 'в работе', theme: 'honey', icon: FilePen},
    {filter: PROGRAM_FILTERS.done, label: 'готовы к утверждению', theme: 'mint', icon: FileCheck2},
]);

const props = defineProps({
    /** @type {import('vue').PropType<Record<string, number>>} */
    counts: {type: Object, required: true},
});

const model = defineModel({type: String, required: true});

const tiles = computed(() => TILES.map((tile) => ({...tile, count: props.counts[tile.filter]})));
</script>

<template>
    <div
        class="programs-tiles"
        role="group"
        aria-label="Показать программы"
    >
        <button
            v-for="tile in tiles"
            :key="tile.filter"
            type="button"
            :class="[
                'programs-tiles__tile',
                `programs-tiles__tile--${tile.theme}`,
                {'programs-tiles__tile--active': model === tile.filter},
            ]"
            :aria-pressed="model === tile.filter"
            @click="model = tile.filter"
        >
            <span class="programs-tiles__text">
                <span class="programs-tiles__count">{{ tile.count }}</span>
                <span class="programs-tiles__label">{{ tile.label }}</span>
            </span>
            <span class="programs-tiles__icon">
                <component
                    :is="tile.icon"
                    :size="32"
                    aria-hidden="true"
                />
            </span>
        </button>
    </div>
</template>

<style lang="scss">
$tile-min-height: 148px;
$tile-radius: 24px;
$icon-size: 72px;

.programs-tiles {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: $indent-step * 4;

    &__tile {
        display: flex;
        align-items: flex-end;
        justify-content: space-between;
        min-height: $tile-min-height;
        text-align: left;
        border: 2px solid transparent;
        border-radius: $tile-radius;
        gap: $indent-step * 4;

        @include lift;
        @include padding('y', 5);
        @include padding('x', 6);

        &--white {
            color: $color-ink;
            background-color: $color-surface;
        }

        &--honey {
            color: $color-honey-ink;
            background-color: $color-honey;
        }

        &--mint {
            color: $color-pine;
            background-color: $color-mint-line;
        }

        &--active {
            border-color: $color-pine;
        }
    }

    &__text {
        @include column($indent-step * 1.5);
    }

    &__count {
        letter-spacing: -0.04em;
        font-size: 64px;
        font-weight: $font-weight-extrabold;
        line-height: 0.95;
        font-variant-numeric: tabular-nums;
    }

    &__label {
        font-weight: $font-weight-bold;
    }

    &__icon {
        flex: none;
        width: $icon-size;
        height: $icon-size;
        border-radius: $radius-tile;
        background-color: rgba($color-white, 55%);

        @include flex-center;
    }

    @include mobile {
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: $indent-step * 2;

        &__tile {
            min-height: 0;

            @include padding('y', 3);
            @include padding('x', 3);
        }

        &__count {
            font-size: $font-size-xxl;
        }

        &__label {
            font-size: $font-size-xs;
        }

        &__icon {
            display: none;
        }
    }
}
</style>

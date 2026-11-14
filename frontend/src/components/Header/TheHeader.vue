<script setup>
import {storeToRefs} from 'pinia';
import {computed} from 'vue';
import {useRoute} from 'vue-router';
import {Search} from 'lucide-vue-next';
import {ROUTE_NAMES} from '@/core/constants';
import {useProgramsStore} from '@/core/stores/programs';

import logoUrl from '@/assets/images/logo.webp';

const route = useRoute();
const {searchQuery} = storeToRefs(useProgramsStore());

const isSearchVisible = computed(() => route.name === ROUTE_NAMES.programs);
const isProgramsSection = computed(() => Object.values(ROUTE_NAMES).includes(route.name));
</script>

<template>
    <header class="header">
        <RouterLink
            class="header__brand"
            :to="{name: ROUTE_NAMES.programs}"
        >
            <img
                class="header__logo"
                :src="logoUrl"
                alt=""
            />
            <span class="header__names">
                <span class="header__name">Конструктор РПД</span>
                <span class="header__tagline">рабочие программы дисциплин</span>
            </span>
        </RouterLink>
        <nav
            class="header__nav"
            aria-label="Основная навигация"
        >
            <RouterLink
                :class="['header__link', {'header__link--active': isProgramsSection}]"
                :to="{name: ROUTE_NAMES.programs}"
            >
                Программы
            </RouterLink>
        </nav>
        <label
            v-if="isSearchVisible"
            class="header__search"
        >
            <Search
                :size="20"
                aria-hidden="true"
            />
            <input
                v-model="searchQuery"
                class="header__search-input"
                type="search"
                placeholder="Найдите программу или дисциплину"
                aria-label="Поиск программы или дисциплины"
            />
        </label>
    </header>
</template>

<style lang="scss">
$logo-size: 44px;
$search-width: 340px;

.header {
    display: flex;
    align-items: center;
    flex: none;
    min-height: $header-height;
    margin: ($indent-step * 4) $page-gutter 0;
    border: 1px solid $color-line;
    border-radius: $radius-chip;
    background-color: $color-surface;
    box-shadow: $shadow-card;
    gap: $indent-step * 4;

    @include padding('x', 3);

    &__brand {
        display: flex;
        align-items: center;
        gap: $indent-step * 3;
    }

    &__logo {
        width: $logo-size;
        height: $logo-size;
        border-radius: 50%;
        object-fit: cover;
    }

    &__names {
        display: flex;
        flex-direction: column;
    }

    &__name {
        font-size: $font-size-md;
        font-weight: $font-weight-bold;
        line-height: 1.3;
    }

    &__tagline {
        color: $color-ink-soft;
        font-size: $font-size-xs;
        line-height: 1.3;
    }

    &__nav {
        display: flex;
        flex: 1;
        margin-left: $indent-step * 4;
        gap: $indent-step;
    }

    &__link {
        display: inline-flex;
        align-items: center;
        height: $control-height-sm + $indent-step;
        transition: background-color $duration ease;
        color: $color-ink-soft;
        border-radius: $radius-chip;
        font-size: $font-size-sm + 1px;
        font-weight: $font-weight-semibold;

        @include padding('x', 4);

        @include hover {
            background-color: $color-surface-muted;
        }

        &--active {
            color: $color-white;
            background-color: $color-teal;
            font-weight: $font-weight-bold;
        }
    }

    &__search {
        display: flex;
        align-items: center;
        width: $search-width;
        height: $control-height-sm + $indent-step;
        transition:
            border-color $duration ease,
            background-color $duration ease;
        color: $color-ink-soft;
        border: 1px solid transparent;
        border-radius: $radius-chip;
        background-color: $color-surface-muted;
        gap: $indent-step * 2;

        @include padding('x', 4);

        &:focus-within {
            border-color: $color-teal;
            background-color: $color-surface;
            box-shadow: 0 0 0 1px $color-teal;
        }
    }

    &__search-input {
        flex: 1;
        min-width: 0;
        color: $color-ink;
        border: none;
        outline: none;
        background: transparent;
        font: inherit;
        font-size: $font-size-sm + 1px;

        &::placeholder {
            color: $color-ink-soft;
        }
    }

    @include tablet {
        flex-wrap: wrap;
        border-radius: $radius-card;

        @include padding('y', 2);

        &__search {
            width: 100%;
        }
    }

    @include mobile {
        margin: ($indent-step * 2) ($indent-step * 2) 0;

        &__tagline,
        &__nav {
            display: none;
        }

        &__brand {
            flex: 1;
        }
    }
}
</style>

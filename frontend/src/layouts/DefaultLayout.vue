<script setup>
import {useProgramsStore} from '@/core/stores/programs';

import TheHeader from '@/components/Header/TheHeader.vue';

const programsStore = useProgramsStore();

programsStore.restore();
</script>

<template>
    <div class="layout">
        <TheHeader />
        <main class="layout__main">
            <slot />
        </main>
    </div>
</template>

<style lang="scss">
.layout {
    display: flex;
    flex-direction: column;
    max-width: $page-max-width;
    min-height: 100vh;
    margin: 0 auto;

    &__main {
        display: flex;
        flex: 1;
        flex-direction: column;
        min-width: 0;
    }
}
</style>

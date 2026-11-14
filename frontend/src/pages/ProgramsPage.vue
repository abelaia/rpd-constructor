<script setup>
import {storeToRefs} from 'pinia';
import {computed, ref} from 'vue';
import {useRouter} from 'vue-router';
import {Plus} from 'lucide-vue-next';
import {PROGRAM_FILTERS, ROUTE_NAMES, START_MODES} from '@/core/constants';
import {useProgramsStore} from '@/core/stores/programs';
import {useToastStore} from '@/core/stores/toast';
import {useDownloadProgram} from '@/composables/useDownloadProgram';

import DeleteProgramDialog from '@/components/Programs/DeleteProgramDialog.vue';
import NewProgramDialog from '@/components/Programs/NewProgramDialog.vue';
import ProgramFolder from '@/components/Programs/ProgramFolder.vue';
import ProgramsEmpty from '@/components/Programs/ProgramsEmpty.vue';
import ProgramsHero from '@/components/Programs/ProgramsHero.vue';
import ProgramsTiles from '@/components/Programs/ProgramsTiles.vue';

const TITLES = Object.freeze({
    [PROGRAM_FILTERS.all]: 'Недавние программы',
    [PROGRAM_FILTERS.inProgress]: 'Программы в работе',
    [PROGRAM_FILTERS.done]: 'Готовые программы',
});

const router = useRouter();
const programsStore = useProgramsStore();
const toastStore = useToastStore();
const {programs, sortedPrograms, visiblePrograms, counts, filter, latestProgram} = storeToRefs(programsStore);
const {isDownloading, download} = useDownloadProgram();

/** @type {import('vue').Ref<string | null>} */
const newProgramMode = ref(null);
/** @type {import('vue').Ref<import('@/core/types/program').Program | null>} */
const programToRemove = ref(null);
const downloadingId = ref('');

const hasPrograms = computed(() => programs.value.length > 0);
const title = computed(() => TITLES[filter.value]);

function handleCreate() {
    newProgramMode.value = START_MODES.blank;
}

function handleCopy() {
    newProgramMode.value = START_MODES.copy;
}

function handleDialogClose() {
    newProgramMode.value = null;
}

/** @param {import('@/core/types/program').Program} program */
function handleCreated(program) {
    newProgramMode.value = null;
    router.push({name: ROUTE_NAMES.editor, params: {id: program.id}});
}

/** @param {import('@/core/types/program').Program} program */
async function handleDownload(program) {
    downloadingId.value = program.id;
    await download(program);
    downloadingId.value = '';
}

/** @param {import('@/core/types/program').Program} program */
function handleDuplicate(program) {
    programsStore.duplicateProgram(program.id);
    toastStore.show('Копия программы создана');
}

/** @param {import('@/core/types/program').Program} program */
function handleRemoveRequest(program) {
    programToRemove.value = program;
}

function handleRemoveCancel() {
    programToRemove.value = null;
}

/** @param {import('@/core/types/program').Program} program */
function handleRemoveConfirm(program) {
    programsStore.removeProgram(program.id);
    programToRemove.value = null;
    toastStore.show('Программа удалена');
}
</script>

<template>
    <div class="programs-page">
        <ProgramsHero
            :latest-program="latestProgram"
            :has-programs="hasPrograms"
            @create="handleCreate"
            @copy="handleCopy"
        />
        <ProgramsEmpty
            v-if="!hasPrograms"
            @create="handleCreate"
        />
        <template v-else>
            <ProgramsTiles
                v-model="filter"
                :counts="counts"
            />
            <h2 class="programs-page__title">{{ title }}</h2>
            <ProgramsEmpty
                v-if="visiblePrograms.length === 0"
                is-filtered
            />
            <div
                v-else
                class="programs-page__grid"
            >
                <ProgramFolder
                    v-for="program in visiblePrograms"
                    :key="program.id"
                    :program="program"
                    :is-downloading="isDownloading && downloadingId === program.id"
                    @download="handleDownload"
                    @duplicate="handleDuplicate"
                    @remove="handleRemoveRequest"
                />
                <button
                    type="button"
                    class="programs-page__new"
                    @click="handleCreate"
                >
                    <Plus
                        :size="24"
                        aria-hidden="true"
                    />
                    Новая программа
                    <span class="programs-page__new-hint">с нуля, из своей или из шаблона кафедры</span>
                </button>
            </div>
        </template>
        <NewProgramDialog
            v-if="newProgramMode"
            :initial-mode="newProgramMode"
            :programs="sortedPrograms"
            @close="handleDialogClose"
            @created="handleCreated"
        />
        <DeleteProgramDialog
            v-if="programToRemove"
            :program="programToRemove"
            @close="handleRemoveCancel"
            @confirm="handleRemoveConfirm"
        />
    </div>
</template>

<style lang="scss">
$folder-min-width: 340px;
$new-min-height: 180px;
$tab-offset: 28px;

.programs-page {
    @include column($indent-step * 6);
    @include padding('top', 6);
    @include padding('x', 6);
    @include padding('bottom', 12);

    &__title {
        margin-top: $indent-step * 2;

        @include display($font-size-xxl);
    }

    &__grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax($folder-min-width, 1fr));
        gap: ($indent-step * 4) ($indent-step * 5);
    }

    &__new {
        align-items: center;
        justify-content: center;
        min-height: $new-min-height;
        margin-top: $tab-offset;
        transition:
            border-color $duration ease,
            background-color $duration ease;
        color: $color-teal;
        border: 1.5px dashed $color-ink-faint;
        border-radius: $radius-card;
        background: transparent;
        font-weight: $font-weight-bold;

        @include column($indent-step * 1.5);
        @include padding('x', 5);

        @include hover {
            border-color: $color-teal;
            background-color: $color-mint;
        }
    }

    &__new-hint {
        @include caption;
    }

    @include mobile {
        @include padding('top', 4);
        @include padding('x', 2);

        &__grid {
            grid-template-columns: minmax(0, 1fr);
        }

        &__title {
            font-size: $font-size-xl;
        }
    }
}
</style>

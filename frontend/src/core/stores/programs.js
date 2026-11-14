import {defineStore} from 'pinia';
import {computed, ref} from 'vue';
import {PROGRAM_FILTERS, START_MODES} from '@/core/constants';
import {DEPARTMENT_TEMPLATE} from '@/core/data/catalog';
import {createId} from '@/core/helpers/createId';
import {loadPrograms, savePrograms} from '@/core/helpers/programsStorage';
import {createProgram, isProgramDone} from '@/core/utils/programs';

/** @typedef {import('@/core/types/program').Program} Program */
/** @typedef {import('@/core/types/program').NewProgramForm} NewProgramForm */

const COPY_SUFFIX = ' — копия';

/** @returns {string} */
function getNow() {
    return new Date().toISOString();
}

/**
 * @param {Program} source
 * @param {string} name
 * @returns {Program}
 */
function cloneProgram(source, name) {
    const now = getNow();

    return {...structuredClone(source), id: createId(), createdAt: now, changedAt: now, disciplineName: name};
}

export const useProgramsStore = defineStore('programs', () => {
    /** @type {import('vue').Ref<Program[]>} */
    const programs = ref([]);
    const searchQuery = ref('');
    const filter = ref(PROGRAM_FILTERS.all);
    const isRestored = ref(false);

    const sortedPrograms = computed(() =>
        [...programs.value].sort((first, second) => second.changedAt.localeCompare(first.changedAt)),
    );

    const counts = computed(() => {
        const doneCount = programs.value.filter(isProgramDone).length;

        return {
            [PROGRAM_FILTERS.all]: programs.value.length,
            [PROGRAM_FILTERS.inProgress]: programs.value.length - doneCount,
            [PROGRAM_FILTERS.done]: doneCount,
        };
    });

    const visiblePrograms = computed(() => {
        const query = searchQuery.value.trim().toLowerCase();

        return sortedPrograms.value.filter((program) => {
            const isMatchingFilter =
                filter.value === PROGRAM_FILTERS.all ||
                isProgramDone(program) === (filter.value === PROGRAM_FILTERS.done);
            const isMatchingQuery =
                query === '' || `${program.disciplineName} ${program.code}`.toLowerCase().includes(query);

            return isMatchingFilter && isMatchingQuery;
        });
    });

    const latestProgram = computed(() => sortedPrograms.value[0] ?? null);

    function restore() {
        if (isRestored.value) {
            return;
        }

        programs.value = loadPrograms();
        isRestored.value = true;
    }

    /**
     * @param {string} id
     * @returns {Program | null}
     */
    function getProgram(id) {
        return programs.value.find((program) => program.id === id) ?? null;
    }

    /** @param {Program[]} nextPrograms */
    function setPrograms(nextPrograms) {
        programs.value = nextPrograms;
        savePrograms(nextPrograms);
    }

    /**
     * @param {NewProgramForm} form
     * @returns {Program}
     */
    function addProgram({name, mode, sourceId}) {
        const source = mode === START_MODES.copy && sourceId ? getProgram(sourceId) : null;
        const blank = createProgram({id: createId(), name, now: getNow()});
        const templated =
            mode === START_MODES.template ? {...blank, sections: {...blank.sections, ...DEPARTMENT_TEMPLATE}} : blank;
        const program = source ? cloneProgram(source, name.trim()) : templated;

        setPrograms([...programs.value, program]);

        return program;
    }

    /**
     * @param {string} id
     * @param {Partial<Program>} patch
     */
    function updateProgram(id, patch) {
        setPrograms(
            programs.value.map((program) =>
                program.id === id ? {...program, ...patch, changedAt: getNow()} : program,
            ),
        );
    }

    /** @param {string} id */
    function duplicateProgram(id) {
        const source = getProgram(id);

        if (!source) {
            return;
        }

        setPrograms([...programs.value, cloneProgram(source, `${source.disciplineName}${COPY_SUFFIX}`)]);
    }

    /** @param {string} id */
    function removeProgram(id) {
        setPrograms(programs.value.filter((program) => program.id !== id));
    }

    return {
        programs,
        searchQuery,
        filter,
        isRestored,
        sortedPrograms,
        counts,
        visiblePrograms,
        latestProgram,
        restore,
        getProgram,
        addProgram,
        updateProgram,
        duplicateProgram,
        removeProgram,
    };
});

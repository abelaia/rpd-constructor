import {computed} from 'vue';
import {useRoute, useRouter} from 'vue-router';
import {ROUTE_NAMES, TITLE_SECTION_ID} from '@/core/constants';
import {SECTIONS} from '@/core/data/sections';
import {useProgramsStore} from '@/core/stores/programs';
import {formatTime} from '@/core/utils/format';
import {getDoneCount, getSectionStatuses} from '@/core/utils/programs';

/** @typedef {import('@/core/types/program').Program} Program */
/** @typedef {import('@/core/types/program').ProgramSections} ProgramSections */

export function useProgramEditor() {
    const route = useRoute();
    const router = useRouter();
    const programsStore = useProgramsStore();

    const programId = computed(() => String(route.params.id));
    const program = computed(() => programsStore.getProgram(programId.value));
    const activeIndex = computed(() => {
        const index = SECTIONS.findIndex((section) => section.id === route.params.section);

        return index === -1 ? 0 : index;
    });
    const activeSection = computed(() => SECTIONS[activeIndex.value]);
    const previousSection = computed(() => SECTIONS[activeIndex.value - 1] ?? null);
    const nextSection = computed(() => SECTIONS[activeIndex.value + 1] ?? null);
    const statuses = computed(() => (program.value ? getSectionStatuses(program.value) : {}));
    const doneCount = computed(() => (program.value ? getDoneCount(program.value) : 0));
    const savedAtLabel = computed(() => (program.value ? `Сохранено в ${formatTime(program.value.changedAt)}` : ''));

    /** @param {Partial<Program>} patch */
    function update(patch) {
        programsStore.updateProgram(programId.value, patch);
    }

    /** @param {Partial<ProgramSections>} patch */
    function updateSections(patch) {
        if (!program.value) {
            return;
        }

        update({sections: {...program.value.sections, ...patch}});
    }

    /** @param {string} sectionId */
    function openSection(sectionId) {
        router.push({
            name: ROUTE_NAMES.editor,
            params: {id: programId.value, section: sectionId === TITLE_SECTION_ID ? undefined : sectionId},
        });
    }

    return {
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
    };
}

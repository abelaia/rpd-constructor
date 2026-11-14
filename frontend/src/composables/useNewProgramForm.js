import {ref} from 'vue';
import {useProgramsStore} from '@/core/stores/programs';
import {validateProgramName, validateSource} from '@/core/utils/programValidation';

/**
 * @param {string} initialMode значение из START_MODES
 * @param {(program: import('@/core/types/program').Program) => void} onCreated
 */
export function useNewProgramForm(initialMode, onCreated) {
    const programsStore = useProgramsStore();

    const name = ref('');
    const mode = ref(initialMode);
    const sourceId = ref('');
    /** @type {import('vue').Ref<string | null>} */
    const nameError = ref(null);
    /** @type {import('vue').Ref<string | null>} */
    const sourceError = ref(null);

    function submit() {
        nameError.value = validateProgramName(name.value);
        sourceError.value = validateSource(mode.value, sourceId.value);

        if (nameError.value || sourceError.value) {
            return;
        }

        onCreated(programsStore.addProgram({name: name.value, mode: mode.value, sourceId: sourceId.value}));
    }

    return {name, mode, sourceId, nameError, sourceError, submit};
}

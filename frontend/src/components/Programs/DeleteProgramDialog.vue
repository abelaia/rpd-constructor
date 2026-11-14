<script setup>
import {computed} from 'vue';

import UiButton from '@/components/Ui/UiButton.vue';
import UiModal from '@/components/Ui/UiModal.vue';

const props = defineProps({
    /** @type {import('vue').PropType<import('@/core/types/program').Program>} */
    program: {type: Object, required: true},
});

const emit = defineEmits(['close', 'confirm']);

const description = computed(
    () => `«${props.program.disciplineName}» и её черновик будут удалены. Вернуть их не получится.`,
);
</script>

<template>
    <UiModal
        title="Удалить программу?"
        :description="description"
        @close="emit('close')"
    >
        <div class="delete-program">
            <UiButton
                theme="text"
                @click="emit('close')"
            >
                Оставить
            </UiButton>
            <UiButton
                theme="danger"
                @click="emit('confirm', program)"
            >
                Удалить
            </UiButton>
        </div>
    </UiModal>
</template>

<style lang="scss">
.delete-program {
    display: flex;
    justify-content: flex-end;
    gap: $indent-step * 2;
}
</style>

<script setup>
import UiField from '@/components/Ui/UiField.vue';

const TEXT_ROWS = 14;

const props = defineProps({
    /** @type {import('vue').PropType<import('@/core/types/program').Program>} */
    program: {type: Object, required: true},
    /** @type {import('vue').PropType<import('@/core/types/program').SectionInfo>} */
    section: {type: Object, required: true},
});

const emit = defineEmits(['update', 'update-sections']);

/** @param {string} value */
function handleUpdate(value) {
    emit('update-sections', {[props.section.field]: value});
}
</script>

<template>
    <UiField
        :model-value="program.sections[section.field]"
        label="Текст раздела"
        hint="Каждый абзац — с новой строки. Строки с дефиса станут списком."
        :placeholder="section.placeholder"
        :rows="TEXT_ROWS"
        @update:model-value="handleUpdate"
    />
</template>

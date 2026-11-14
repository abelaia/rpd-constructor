<script setup>
import {EQUIPMENT_COLUMNS} from '@/core/data/tables';

import EditorTable from '@/components/Editor/EditorTable.vue';
import UiField from '@/components/Ui/UiField.vue';

const INTRO_ROWS = 3;

defineProps({
    /** @type {import('vue').PropType<import('@/core/types/program').Program>} */
    program: {type: Object, required: true},
});

const emit = defineEmits(['update', 'update-sections']);
</script>

<template>
    <div class="section-equipment">
        <UiField
            :model-value="program.sections.equipmentIntro"
            label="Вводный текст"
            placeholder="При реализации дисциплины используются следующие помещения, оборудование и программное обеспечение:"
            :rows="INTRO_ROWS"
            @update:model-value="emit('update-sections', {equipmentIntro: $event})"
        />
        <EditorTable
            caption="Оснащение"
            item-label="Строка"
            add-label="Добавить строку"
            :columns="EQUIPMENT_COLUMNS"
            :rows="program.sections.equipment"
            @update:rows="emit('update-sections', {equipment: $event})"
        />
    </div>
</template>

<style lang="scss">
.section-equipment {
    @include column($indent-step * 5);
}
</style>

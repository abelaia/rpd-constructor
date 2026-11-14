<script setup>
import UiField from '@/components/Ui/UiField.vue';

const FIELDS = Object.freeze([
    {key: 'disciplineName', label: 'Название дисциплины (рус.)', hint: 'Как в учебном плане', isWide: true},
    {key: 'disciplineNameEn', label: 'Название (англ.)', hint: 'Например: Databases', isWide: true},
    {key: 'code', label: 'Код', hint: 'Из учебного плана, например: Б1.О.14'},
    {key: 'semester', label: 'Семестр', hint: 'Например: 5 семестр'},
    {key: 'teacherName', label: 'Составитель', hint: 'Инициалы и фамилия, например: М. С. Белова'},
    {key: 'teacherTitle', label: 'Учёная степень, должность', hint: 'Например: канд. техн. наук, доцент'},
    {key: 'department', label: 'Кафедра', hint: 'Без слова «кафедра», например: Информационных систем', isWide: true},
    {key: 'umsDate', label: 'Дата протокола УМС', hint: 'Например: «28» августа 2026 г.'},
    {key: 'umsProtocol', label: 'Номер протокола УМС', hint: 'Только номер, например: 1'},
]);

defineProps({
    /** @type {import('vue').PropType<import('@/core/types/program').Program>} */
    program: {type: Object, required: true},
});

const emit = defineEmits(['update', 'update-sections']);

/**
 * @param {string} key
 * @param {string} value
 */
function handleUpdate(key, value) {
    emit('update', {[key]: value});
}
</script>

<template>
    <div class="section-title">
        <UiField
            v-for="field in FIELDS"
            :key="field.key"
            :class="{'section-title__wide': field.isWide}"
            :model-value="program[field.key]"
            :label="field.label"
            :hint="field.hint"
            @update:model-value="handleUpdate(field.key, $event)"
        />
    </div>
</template>

<style lang="scss">
.section-title {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: ($indent-step * 4) ($indent-step * 5);

    &__wide {
        grid-column: 1 / -1;
    }

    @include mobile {
        grid-template-columns: minmax(0, 1fr);
    }
}
</style>

<script setup>
import UiField from '@/components/Ui/UiField.vue';

const FIELDS = Object.freeze([
    {
        key: 'mainLiterature',
        label: 'Основная литература',
        placeholder: '1. Фамилия, И. О. Название. — Город : Издательство, 2024. — 320 с.',
        rows: 6,
    },
    {key: 'additionalLiterature', label: 'Дополнительная литература', placeholder: '1. …', rows: 5},
    {
        key: 'internetResources',
        label: 'Интернет-ресурсы',
        placeholder: '1. Название ресурса. — URL: https://… (дата обращения: 01.09.2026)',
        rows: 4,
    },
]);

defineProps({
    /** @type {import('vue').PropType<import('@/core/types/program').Program>} */
    program: {type: Object, required: true},
});

const emit = defineEmits(['update', 'update-sections']);
</script>

<template>
    <div class="section-literature">
        <UiField
            v-for="field in FIELDS"
            :key="field.key"
            :model-value="program.sections[field.key]"
            :label="field.label"
            :placeholder="field.placeholder"
            :rows="field.rows"
            hint="Каждый источник — с новой строки"
            @update:model-value="emit('update-sections', {[field.key]: $event})"
        />
    </div>
</template>

<style lang="scss">
.section-literature {
    @include column($indent-step * 5);
}
</style>

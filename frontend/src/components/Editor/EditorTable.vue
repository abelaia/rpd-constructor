<script setup>
import {computed, nextTick, ref} from 'vue';
import {GripVertical, Plus, Trash2} from 'lucide-vue-next';
import {createId} from '@/core/helpers/createId';
import {createRow, moveRow, removeRow, updateRow} from '@/core/utils/rows';

const SERVICE_COLUMNS_START = '36px 32px';
const SERVICE_COLUMNS_END = '40px';

const props = defineProps({
    caption: {type: String, required: true},
    /** @type {import('vue').PropType<readonly import('@/core/types/program').TableColumn[]>} */
    columns: {type: Array, required: true},
    /** @type {import('vue').PropType<Array<{id: string} & Record<string, string>>>} */
    rows: {type: Array, required: true},
    addLabel: {type: String, required: true},
    itemLabel: {type: String, required: true},
    /** @type {import('vue').PropType<Record<string, string> | null>} */
    totals: {type: Object, default: null},
});

const emit = defineEmits(['update:rows']);

/** @type {import('vue').Ref<number | null>} */
const dragIndex = ref(null);
/** @type {import('vue').Ref<number | null>} */
const dropIndex = ref(null);
/** @type {Map<string, HTMLElement>} */
const gripElements = new Map();

const gridTemplate = computed(() =>
    [SERVICE_COLUMNS_START, ...props.columns.map((column) => column.width ?? '1fr'), SERVICE_COLUMNS_END].join(' '),
);
const columnKeys = computed(() => props.columns.map((column) => column.key));

/**
 * @param {string} id
 * @param {string} key
 * @param {string} value
 */
function handleInput(id, key, value) {
    emit('update:rows', updateRow(props.rows, id, key, value));
}

function handleAdd() {
    emit('update:rows', [...props.rows, createRow(createId(), columnKeys.value)]);
}

/** @param {string} id */
function handleRemove(id) {
    emit('update:rows', removeRow(props.rows, id));
}

/**
 * @param {number} fromIndex
 * @param {number} toIndex
 */
async function move(fromIndex, toIndex) {
    const nextRows = moveRow(props.rows, fromIndex, toIndex);

    if (nextRows === props.rows) {
        return;
    }

    const movedId = props.rows[fromIndex].id;
    emit('update:rows', nextRows);
    await nextTick();
    gripElements.get(movedId)?.focus();
}

/**
 * @param {KeyboardEvent} event
 * @param {number} index
 */
function handleGripKeydown(event, index) {
    const step = {ArrowUp: -1, ArrowDown: 1}[event.key];

    if (!step) {
        return;
    }

    event.preventDefault();
    move(index, index + step);
}

/**
 * @param {DragEvent} event
 * @param {number} index
 */
function handleDragStart(event, index) {
    dragIndex.value = index;
    event.dataTransfer?.setData('text/plain', String(index));
}

/** @param {number} index */
function handleDragOver(index) {
    if (dragIndex.value !== null) {
        dropIndex.value = index;
    }
}

/** @param {number} index */
function handleDrop(index) {
    if (dragIndex.value !== null) {
        move(dragIndex.value, index);
    }

    handleDragEnd();
}

function handleDragEnd() {
    dragIndex.value = null;
    dropIndex.value = null;
}

/**
 * @param {string} id
 * @returns {(element: HTMLElement | null) => void}
 */
function setGripElement(id) {
    return (element) => {
        if (element) {
            gripElements.set(id, element);

            return;
        }

        gripElements.delete(id);
    };
}
</script>

<template>
    <div
        class="editor-table"
        :style="{'--columns': gridTemplate}"
    >
        <div class="editor-table__scroll">
            <div
                class="editor-table__grid"
                role="table"
                :aria-label="caption"
            >
                <div
                    class="editor-table__row editor-table__row--head"
                    role="row"
                >
                    <span role="columnheader">
                        <span class="editor-table__hidden">Порядок</span>
                    </span>
                    <span
                        class="editor-table__numeric"
                        role="columnheader"
                    >
                        №
                    </span>
                    <span
                        v-for="column in columns"
                        :key="column.key"
                        :class="{'editor-table__numeric': column.isNumeric}"
                        role="columnheader"
                    >
                        {{ column.label }}
                    </span>
                    <span role="columnheader">
                        <span class="editor-table__hidden">Удалить</span>
                    </span>
                </div>
                <div
                    v-for="(row, index) in rows"
                    :key="row.id"
                    :class="[
                        'editor-table__row',
                        {
                            'editor-table__row--dragging': dragIndex === index,
                            'editor-table__row--drop': dropIndex === index && dragIndex !== index,
                        },
                    ]"
                    role="row"
                    @dragover.prevent="handleDragOver(index)"
                    @drop.prevent="handleDrop(index)"
                >
                    <span role="cell">
                        <button
                            :ref="setGripElement(row.id)"
                            type="button"
                            class="editor-table__grip"
                            draggable="true"
                            :aria-label="`${itemLabel} ${index + 1}: переместить стрелками вверх и вниз`"
                            @keydown="handleGripKeydown($event, index)"
                            @dragstart="handleDragStart($event, index)"
                            @dragend="handleDragEnd"
                        >
                            <GripVertical
                                :size="16"
                                aria-hidden="true"
                            />
                        </button>
                    </span>
                    <span
                        class="editor-table__numeric editor-table__index"
                        role="cell"
                    >
                        {{ index + 1 }}
                    </span>
                    <span
                        v-for="(column, columnIndex) in columns"
                        :key="column.key"
                        :class="['editor-table__cell', {'editor-table__cell--wide': columnIndex === 0}]"
                        role="cell"
                    >
                        <label
                            class="editor-table__cell-label"
                            :for="`${row.id}-${column.key}`"
                        >
                            {{ column.label }}
                        </label>
                        <input
                            :id="`${row.id}-${column.key}`"
                            :class="['editor-table__input', {'editor-table__input--numeric': column.isNumeric}]"
                            :value="row[column.key]"
                            :inputmode="column.isNumeric ? 'decimal' : undefined"
                            @input="handleInput(row.id, column.key, $event.target.value)"
                        />
                    </span>
                    <span role="cell">
                        <button
                            type="button"
                            class="editor-table__remove"
                            :aria-label="`Удалить: ${itemLabel.toLowerCase()} ${index + 1}`"
                            @click="handleRemove(row.id)"
                        >
                            <Trash2
                                :size="16"
                                aria-hidden="true"
                            />
                        </button>
                    </span>
                </div>
                <div
                    v-if="totals && rows.length > 0"
                    class="editor-table__row editor-table__row--total"
                    role="row"
                >
                    <span role="cell" />
                    <span role="cell" />
                    <span
                        v-for="column in columns"
                        :key="column.key"
                        :class="{'editor-table__numeric': column.isNumeric}"
                        role="cell"
                    >
                        {{ totals[column.key] ?? '' }}
                    </span>
                    <span role="cell" />
                </div>
            </div>
        </div>
        <button
            type="button"
            class="editor-table__add"
            @click="handleAdd"
        >
            <Plus
                :size="16"
                aria-hidden="true"
            />
            {{ addLabel }}
        </button>
    </div>
</template>

<style lang="scss">
$row-min-height: 52px;
$table-min-width: 760px;
$service-size: 36px;

.editor-table {
    $block: &;

    @include column($indent-step * 2);

    &__scroll {
        overflow-x: auto;
    }

    &__grid {
        min-width: $table-min-width;
    }

    &__row {
        display: grid;
        align-items: center;
        min-height: $row-min-height;
        transition: background-color $duration-fast ease;
        border-bottom: 1px solid $color-line;
        grid-template-columns: var(--columns);
        column-gap: $indent-step * 2;

        @include padding('x', 2);

        @include hover {
            background-color: $color-row-hover;

            #{$block}__grip,
            #{$block}__remove {
                color: $color-ink-soft;
            }
        }

        &--head {
            min-height: $control-height-sm + $indent-step;
            color: $color-ink-soft;
            border-bottom: none;
            border-radius: $radius-field $radius-field 0 0;
            background-color: $color-surface-muted;
            font-size: $font-size-xs;
            font-weight: $font-weight-bold;

            @include hover {
                background-color: $color-surface-muted;
            }
        }

        &--total {
            min-height: $row-min-height + $indent-step;
            border-top: 2px solid $color-ink;
            border-bottom: none;
            font-weight: $font-weight-extrabold;

            @include hover {
                background-color: transparent;
            }
        }

        &--dragging {
            opacity: 0.4;
        }

        &--drop {
            box-shadow: inset 0 2px 0 $color-teal;
        }
    }

    &__numeric {
        text-align: right;
        font-variant-numeric: tabular-nums;
    }

    &__index {
        color: $color-ink-soft;
    }

    &__hidden,
    &__cell-label {
        position: absolute;
        overflow: hidden;
        clip: rect(0 0 0 0);
        width: 1px;
        height: 1px;
        white-space: nowrap;
    }

    &__cell {
        min-width: 0;
    }

    &__input {
        width: 100%;
        min-width: 0;
        transition:
            border-color $duration ease,
            background-color $duration ease;
        color: $color-ink;
        border: 1px solid transparent;
        border-radius: $radius-field * 0.8;
        background: transparent;
        font: inherit;
        font-size: $font-size-sm + 1px;

        @include padding('y', 2);
        @include padding('x', 2);

        @include hover {
            border-color: $color-line-strong;
            background-color: $color-surface;
        }

        &:focus {
            border-color: $color-teal;
            outline: none;
            background-color: $color-surface;
            box-shadow: 0 0 0 1px $color-teal;
        }

        &--numeric {
            text-align: right;
            font-variant-numeric: tabular-nums;
        }
    }

    &__grip {
        cursor: grab;
        color: $color-ink-faint;

        @include icon-button($service-size);
    }

    &__remove {
        color: $color-ink-faint;

        @include icon-button($service-size);

        @include hover {
            color: $color-danger;
            background-color: $color-danger-surface;
        }
    }

    &__add {
        display: flex;
        align-items: center;
        align-self: flex-start;
        height: $control-height;
        transition: background-color $duration ease;
        color: $color-teal;
        border: 1.5px dashed $color-mint-line;
        border-radius: $radius-chip;
        background: transparent;
        font-weight: $font-weight-bold;
        gap: $indent-step * 2;

        @include padding('x', 5);

        @include hover {
            background-color: $color-mint;
        }
    }

    @include mobile {
        &__scroll {
            overflow: visible;
        }

        &__grid {
            min-width: 0;

            @include column($indent-step * 3);
        }

        &__row {
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: $indent-step * 2;
            border: 1px solid $color-line;
            border-radius: $radius-tile;
            background-color: $color-surface;

            @include padding('y', 3);
            @include padding('x', 3);

            &--head {
                display: none;
            }

            &--total {
                border: none;
                background-color: $color-honey;
            }
        }

        &__cell-label {
            position: static;
            overflow: visible;
            clip: auto;
            width: auto;
            height: auto;
            color: $color-ink-soft;
            font-size: $font-size-xs;
            font-weight: $font-weight-semibold;
        }

        &__cell--wide {
            grid-column: 1 / -1;
        }

        &__input {
            border-color: $color-line-strong;
        }
    }
}
</style>

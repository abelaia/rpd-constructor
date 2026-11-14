<script setup>
import {useToastStore} from '@/core/stores/toast';

import ToastElement from '@/components/toast/ToastElement.vue';

const toastStore = useToastStore();
</script>

<template>
    <TransitionGroup
        tag="div"
        name="toast"
        class="toast-container"
    >
        <ToastElement
            v-for="toast in toastStore.toasts"
            :key="toast.id"
            v-bind="toast"
            @close="toastStore.removeToast"
        />
    </TransitionGroup>
</template>

<style lang="scss">
.toast-container {
    position: fixed;
    z-index: $ui-index-6;
    right: $page-gutter;
    bottom: $page-gutter;
    display: flex;
    align-items: flex-end;
    flex-direction: column;
    max-width: calc(100% - #{$page-gutter * 2});
    pointer-events: none;
    gap: $indent-step * 2;

    .toast {
        display: flex;
        align-items: center;
        color: $color-white;
        border-radius: $radius-panel;
        background-color: $color-pine;
        box-shadow: $shadow-popover;
        font-size: $font-size-sm + 1px;
        font-weight: $font-weight-semibold;
        gap: $indent-step * 2.5;

        @include padding('y', 3);
        @include padding('x', 4);

        &__icon {
            flex-shrink: 0;
            color: $color-amber;
        }

        &-enter-active,
        &-leave-active {
            transition:
                opacity $duration ease,
                transform $duration $ease-out;
        }

        &-enter-from,
        &-leave-to {
            transform: translateY($indent-step * 4);
            opacity: 0;
        }
    }
}
</style>

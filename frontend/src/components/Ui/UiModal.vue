<script setup>
import {
    DialogClose,
    DialogContent,
    DialogDescription,
    DialogOverlay,
    DialogPortal,
    DialogRoot,
    DialogTitle,
} from 'reka-ui';
import {X} from 'lucide-vue-next';

defineProps({
    title: {type: String, required: true},
    description: {type: String, default: ''},
    isWide: {type: Boolean, default: false},
    isSheet: {type: Boolean, default: false},
});

const emit = defineEmits(['close']);

/** @param {boolean} isOpen */
function handleOpenChange(isOpen) {
    if (!isOpen) {
        emit('close');
    }
}
</script>

<template>
    <DialogRoot
        :open="true"
        @update:open="handleOpenChange"
    >
        <DialogPortal>
            <DialogOverlay class="ui-modal" />
            <DialogContent
                :class="['ui-modal__window', {'ui-modal__window--wide': isWide, 'ui-modal__window--sheet': isSheet}]"
            >
                <DialogTitle class="ui-modal__title">{{ title }}</DialogTitle>
                <DialogDescription
                    v-if="description"
                    class="ui-modal__description"
                >
                    {{ description }}
                </DialogDescription>
                <slot />
                <DialogClose
                    class="ui-modal__close"
                    aria-label="Закрыть"
                >
                    <X
                        :size="20"
                        aria-hidden="true"
                    />
                </DialogClose>
            </DialogContent>
        </DialogPortal>
    </DialogRoot>
</template>

<style lang="scss">
$window-width: 440px;
$window-width-wide: 560px;
$window-radius: 28px;

.ui-modal {
    position: fixed;
    z-index: $ui-index-4;
    inset: 0;
    animation: fade-in $duration ease both;
    background-color: $color-overlay;

    &__window {
        position: fixed;
        z-index: $ui-index-4;
        top: 50%;
        left: 50%;
        overflow-y: auto;
        width: min($window-width, calc(100% - #{$page-gutter}));
        max-height: calc(100dvh - #{$page-gutter});
        transform: translate(-50%, -50%);
        animation: fade-in $duration ease both;
        color: $color-ink;
        border-radius: $window-radius;
        background-color: $color-surface;
        box-shadow: $shadow-popover;

        @include column($indent-step * 5);
        @include padding('y', 7);
        @include padding('x', 7);

        &--wide {
            width: min($window-width-wide, calc(100% - #{$page-gutter}));
        }

        &--sheet {
            top: auto;
            bottom: 0;
            width: min($window-width-wide, 100%);
            max-height: 90dvh;
            transform: translateX(-50%);
            animation: sheet-rise $duration-slow $ease-out both;
            border-radius: $window-radius $window-radius 0 0;

            @include padding('x', 4);
            @include padding('y', 6);
        }
    }

    &__title {
        margin: 0;
        padding-right: $control-height;

        @include display($font-size-xxl);
    }

    &__description {
        margin: -($indent-step * 3) 0 0;

        @include caption;
    }

    &__close {
        position: absolute;
        top: $indent-step * 5;
        right: $indent-step * 5;

        @include icon-button;
    }

    @include mobile {
        &__window {
            @include padding('x', 5);
        }
    }
}

@keyframes sheet-rise {
    from {
        transform: translate(-50%, 100%);
    }
}
</style>

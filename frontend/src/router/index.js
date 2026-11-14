import {createRouter, createWebHistory} from 'vue-router';
import {ROUTE_NAMES} from '@/core/constants';

import ProgramsPage from '@/pages/ProgramsPage.vue';

export const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    scrollBehavior(to, from, savedPosition) {
        return savedPosition ?? {top: 0};
    },
    routes: [
        {path: '/', redirect: {name: ROUTE_NAMES.programs}},
        {path: '/programs', name: ROUTE_NAMES.programs, component: ProgramsPage},
        {
            path: '/programs/:id/ready',
            name: ROUTE_NAMES.ready,
            component: () => import('@/pages/ReadyPage.vue'),
        },
        {
            path: '/programs/:id/:section?',
            name: ROUTE_NAMES.editor,
            component: () => import('@/pages/EditorPage.vue'),
        },
        {path: '/:pathMatch(.*)*', redirect: {name: ROUTE_NAMES.programs}},
    ],
});

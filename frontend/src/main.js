import { createApp } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';
import App from './App.vue';

import Login from './components/Login.vue';
import AuthGoogle from './components/AuthGoogle.vue';

const routes = [
    { path: '/login', component: Login },
    { path: '/auth/google', component: AuthGoogle }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

createApp(App).use(router).mount('#app');

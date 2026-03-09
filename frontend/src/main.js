import { createApp } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';
import App from './App.vue';

import Login from './components/auth/Login.vue';
import Register from './components/auth/Register.vue';
import AuthGoogle from './components/auth/AuthGoogle.vue';
import ProfilePage from './components/profile/ProfilePage.vue';
import ProfileView from './components/profile/ProfileView.vue'


const routes = [
    { path: '/login', component: Login },
    { path: '/register', component: Register },
    { path: '/auth/google', component: AuthGoogle },
    { path: '/profile', component: ProfilePage },
    { path: '/profile/:id', component: ProfileView },
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

createApp(App).use(router).mount('#app');

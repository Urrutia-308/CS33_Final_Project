import { createRouter, createWebHistory } from 'vue-router';
import ScheduleComponent from '../components/ScheduleComponent.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    component: ScheduleComponent
  },
  {
    path: '/schedule',
    name: 'schedule',
    component: () => import('../views/ScheduleView.vue')
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router;
import { createRouter, createWebHashHistory } from 'vue-router';
import BroadCast1 from './components/broadcast/broadcast1.vue';
import BroadCast2 from './components/broadcast/broadcast2.vue';
import BroadCast3 from './components/broadcast/broadcast3.vue';
import ContActs1 from './components/contacts/contacts1.vue';
import ContActs2 from './components/contacts/contacts2.vue';                
import AppIntegration from './components/integration/integration.vue';
import LoginPage from './components/login/login.vue';
import SignupPage from './components/signup/signup.vue';
import DashboardView from './views/dashboardview.vue';
import Profile from './views/profile.vue';
import PurchaseHistory from './components/PurchaseHistory/PurchaseHistory.vue';
import ChatbotView from './components/chatbot/chatbotview.vue'; // Ensure this path is correct

const routes = [
  // Public routes
  { path: '/', component: LoginPage },
  { path: '/signup', component: SignupPage },
  { path: '/purchase-history', component: PurchaseHistory },
  // { path: '/', component: PublicView },

  // Protected routes within the dashboard
  {
    path: '/dashboard',
    component: DashboardView,
    meta: { requiresAuth: true },
    children: [
      { path: '/broadcast/broadcast1', component: BroadCast1, name: 'Broadcast1' },
      { path: '/broadcast/broadcast2', component: BroadCast2, name: 'Broadcast2' },
      { path: '/broadcast/broadcast3', component: BroadCast3, name: 'Broadcast3' },
      { path: '/contacts/contacts1', component: ContActs1, name: 'Contacts1' },
      { path: '/contacts/contacts2', component: ContActs2, name: 'Contacts2' },
      { path: '/integration/integration1', component: AppIntegration, name: 'Integration1' },
      { path: '/profile', component: Profile },
      { path: '', redirect: '/broadcast/broadcast2' },
      { path: '/chatbot/chatbotview', component: ChatbotView, name: 'ChatbotView' }, // Updated path
      // Add more routes within the dashboard as needed
    ],
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

// Navigation guard to check for authentication
router.beforeEach((to, from, next) => {
  const loggedIn = localStorage.getItem('token');
  
  if (to.matched.some(record => record.meta.requiresAuth) && !loggedIn) {
    next('/'); // Redirect to login page if not authenticated
  } else {
    next();
  }
});

export default router;

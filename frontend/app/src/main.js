import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import './assets/tailwind.css';
import Toast, { POSITION } from 'vue-toastification';
import 'vue-toastification/dist/index.css'; 


const app = createApp(App);

app.use(Toast, {
    position: POSITION.TOP_RIGHT,
    timeout: 5000,
  });

// Enable devtools in production
app.config.devtools = true;

app.use(router).mount('#app');
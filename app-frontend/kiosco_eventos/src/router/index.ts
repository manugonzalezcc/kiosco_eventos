import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import KioscoInicioView from '../views/KioscoInicioView.vue'
import PanelKioscoView from '../views/PanelKioscoView.vue'


const routes = [
  { path: '/', component: LoginView },
  { path: '/login', component: LoginView },
  { path: '/kiosco-inicio', component: KioscoInicioView },
  { path: '/kiosco-panel', component: PanelKioscoView },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
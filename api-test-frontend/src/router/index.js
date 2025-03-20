import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Register from '../views/Register.vue'
import Login from '../views/Login.vue'
import MatlabCompute from '../views/MatlabCompute.vue'
import Track from '../views/Track.vue'
import Antenna from '../views/Antenna.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/matlab',
    name: 'MatlabCompute',
    component: MatlabCompute
  },
  {
    path: '/track',
    name: 'Track',
    component: Track
  },
  {
    path: '/antenna',
    name: 'Antenna',
    component: Antenna
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
import Vue from 'vue'
import Router from 'vue-router'
import Zukan from '@/components/Zukan'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Zukan',
      component: Zukan
    }
  ]
})

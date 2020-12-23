import Vue from 'vue'
import Router from 'vue-router'
import Home from './components/Home.vue';

Vue.use(Router)


export default new Router({
  mode: 'history',
  base: __dirname,
  routes: [
    {
      path: '/images',
      name: 'images',
      component: () => import("./components/PublicImages.vue")
    },
    {
      path: '/user/profile',
      name: 'MyProfile',
      component: () => import("./components/MyProfile.vue")
    },
    {
      path: '/home',
      name: 'Home',
      component: Home,
    },
    {
      path: '/signup',
      name: 'Signup',
      component: () => import("./components/SignUp.vue"),
    },
  ]
})

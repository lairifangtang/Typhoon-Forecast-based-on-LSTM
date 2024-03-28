import Vue from 'vue'
import VueRouter from 'vue-router'

import RegistView from '../views/RegistView'
import LoginView from '../views/LoginView.vue'
import HomeView from '../views/HomeView.vue'
// import { Message } from "element-ui";


Vue.use(VueRouter)

const routes = [
  {
    path: '/',          // 路径
    redirect: '/login'  // 重定向
  },
  {
    path: '/login',     // 路径
    component: LoginView    // 跳转到的组件
  },
  {
    path:'/regist',
    name:'regist',
    component: RegistView
  },
  {
    path:'/home',
    name:'home',
    component:HomeView
  },
]

const router = new VueRouter({
  mode:'history',
  routes
})

// router.beforeEach((to, from, next) => {
//   let isAuthenticated = !!sessionStorage.getItem('user_Info')
//   // 如果路由要跳转到除了登录和注册的界面的话就判断是否已经登录，如果没有登录就强制跳到登录界面
//   if (to.path !== '/login' && to.path !== '/regist' && !isAuthenticated) {
    
      
//       Message({
//           message: 'Unauthorized！',
//           type: "warning",
//       });
//       next({ path: '/login' })
//   } else next()
// }
// )

export default router

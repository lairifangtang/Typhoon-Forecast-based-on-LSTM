import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementUI from 'element-ui';	// Element 1
import 'element-ui/lib/theme-chalk/index.css'; // Element 2
import axios from 'axios'
import VueAxios from 'vue-axios'
import VueRouter from 'vue-router';
import cookieMixin  from './cookieMixin.js'
import VueCookies from 'vue-cookies';

import * as Echarts from 'echarts'
import BMap from 'vue-baidu-map';

Vue.prototype.BMap = BMap;
Vue.prototype.$echarts = Echarts

Vue.config.productionTip = false

Vue.use(ElementUI) // Element 3
Vue.use(VueRouter)
Vue.use(VueAxios,axios)
Vue.use(BMap, { ak: process.env.VUE_APP_BAIDU_MAPS_API_KEY || 'agNZwShLeFNXIaoXS4wPYd02pKXyvVnt'})
Vue.use(VueCookies)

Vue.mixin(cookieMixin)

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')

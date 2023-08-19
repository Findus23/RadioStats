import  {createApp} from 'vue';
import {router} from "./routes";
import App from "./App.vue";

// Vue.use(VueHead);
// let matomo = new MatomoTracker;
// matomo.init();
//
// let app = new Vue({
//     el: '#app',
//     router,
//     render: h => h(App),
//     comments: true
// });

const app = createApp(App)

app.use(router)

app.mount('#app')

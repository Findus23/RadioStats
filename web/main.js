import Vue from 'vue';
import VueHead from 'vue-head';
import App from './App.vue';
import router from './routes';
import MatomoTracker from './MatomoTracker';

Vue.use(VueHead);

let matomo = new MatomoTracker;
matomo.init();

let app = new Vue({
    el: '#app',
    router,
    render: h => h(App),
    comments: true
});

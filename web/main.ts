import Vue from 'vue';
import Vuex from 'vuex';
import VueHead from 'vue-head';
import App from './App.vue';
import router from './routes';
import MatomoTracker from './MatomoTracker';
import store from './store';

Vue.use(VueHead);

let matomo = new MatomoTracker;
matomo.init();

let app = new Vue({
    el: '#app',
    router,
    store: store,
    render: h => h(App),
    comments: true
});

import Vue from 'vue';
import VueHead from 'vue-head';
import App from './App.vue';
import router from './routes';
import MatomoTracker from './MatomoTracker';
import store from './store';
Vue.use(VueHead);
var matomo = new MatomoTracker;
matomo.init();
var app = new Vue({
    el: '#app',
    router: router,
    store: store,
    render: function (h) { return h(App); },
    comments: true
});

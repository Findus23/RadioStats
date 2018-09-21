import Vue from 'vue';
import VueHead from 'vue-head';
import App from './App.vue';
import router from './routes';
import MatomoTracker from './MatomoTracker';
import {init, Integrations} from '@sentry/browser';

init({
    dsn: 'https://91af780499634f98a17afe160c6ace89@sentry.lw1.at/12',
    integrations: [new Integrations.Vue({Vue})],
    release: COMMIT_HASH
});

Vue.use(VueHead);
let matomo = new MatomoTracker;
matomo.init();

let app = new Vue({
    el: '#app',
    router,
    render: h => h(App),
    comments: true
});

import Vue from 'vue';
import List from './List.vue';
import DetailView from './DetailView.vue';
import Router from 'vue-router';

Vue.use(Router);

let router = new Router({
    mode: 'history',
    routes: [
        {
            path: '/',
            redirect: "/oe3"
        },
        {
            path: '/:channel',
            name: 'List',
            component: List,
            props: true,
            children: [
                {path: '/:channel/song/:songId', component: DetailView, name: 'DetailView'}
            ]
        },
        {
            path: '*',
            redirect: '/'
        }
    ]
});

function trackPageView() {
    Vue.nextTick(function () {
        _paq.push(['setDocumentTitle', document.title]);
        _paq.push(['trackPageView']);
        _paq.push(['enableLinkTracking']);
    });
}

router.afterEach((to, from) => {
    _paq.push(['setCustomUrl', to.fullPath]);
    _paq.push(['setGenerationTimeMs', 0]);
    if (from.matched.length !== 0 && from.fullPath !== "/") {
        _paq.push(['setReferrerUrl', from.fullPath]);
        trackPageView();
    } else {
        setTimeout(trackPageView, 500); // first page load has to finish loading channels before title is set
    }


});
export default router;

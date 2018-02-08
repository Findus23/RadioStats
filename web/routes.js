import Vue from 'vue';
import List from './List.vue';
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
            // children: [
            //     {path: '/:language/:id', component: L, name: 'itemModal'}
            // ]
        },
        {
            path: '*',
            redirect: '/'
        }
    ]
});

router.afterEach((to, from) => {

});
export default router;

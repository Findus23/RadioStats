import Vuex from 'vuex';
import Vue from 'vue';
Vue.use(Vuex);
var state = {
    songs: []
};
var mutations = {};
var actions = {};
export default new Vuex.Store({
    state: state,
    mutations: mutations,
    actions: actions
});

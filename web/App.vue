<template>
    <div id="app" class="container">
        <router-view></router-view>
    </div>
</template>

<script lang="ts">
    import Vue from 'vue';

    export default Vue.extend({
        name: 'app',
        props: ["language"],
    });
</script>

<style lang="css" src="./node_modules/normalize.css/normalize.css">
</style>

<style lang="scss">
    @import "variables";
    @import "node_modules/milligram/src/milligram";
</style>

<template>
    <div id="app" class="container">
        <router-view></router-view>
    </div>
</template>

<script>
// import "./node_modules/normalize.css/normalize.css"

export default {
    name: 'app',
    props: ["language"],
};
</script>

<style lang="scss">
    @import "./variables";
    @import "./node_modules/milligram/src/milligram";

    .iewarning {
        margin: 2rem;
        padding: 2rem;
        background: #f0ad4e;

        a {
            color: inherit;
            font-style: italic;
        }

        p:last-child {
            margin-bottom: 0;
        }
    }
</style>

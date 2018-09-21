<template>
    <footer :style="color">
        <div><a href="https://lw1.at/de/impressum">Impressum</a></div>
        <div><a class="small" href="https://developer.spotify.com/">Albumcover und Probehören mithife von Spotify</a>
        </div>
        <div><a href="https://lw1.at/">Andere Projekte</a></div>
    </footer>
</template>

<script lang="ts">
    import Vue from 'vue';

    export default Vue.extend({
        name: "info",
        props: {
            color: String
        },
    };
</script>

<style lang="scss">
    footer {
        padding: 1rem 2rem;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        a {
            color: inherit;
            font-weight: bold;
            transition: filter .2s;
            &:hover {
                color: inherit;
                filter: invert(30%);
            }
            &.small {
                font-size: 70%;
            }
        }
    }
</style>

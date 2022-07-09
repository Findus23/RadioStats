<template>
    <div class="detailView customRow" :style="{backgroundColor:'#'+song.song.background_color,color:'#'+song.song.text_color}">
        <div>
            <img v-if="song.song.image_large" :src="song.song.image_large">
            <div v-else class="imgPlaceholder">
                <div>?</div>
            </div>
            <audio v-if="song.song.preview_url" controls preload="none" :src="song.song.preview_url"></audio>
            <a v-if="song.song.spotify_url" :href="song.song.spotify_url" class="spotifyLink" target="_blank"
               rel="noopener" :style="{color: '#'+song.song.alternative_color}">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 168 168">
                    <path d="m83.996 0.277c-46.249 0-83.743 37.493-83.743 83.742 0 46.251 37.494 83.741 83.743 83.741 46.254 0 83.744-37.49 83.744-83.741 0-46.246-37.49-83.738-83.745-83.738l0.001-0.004zm38.404 120.78c-1.5 2.46-4.72 3.24-7.18 1.73-19.662-12.01-44.414-14.73-73.564-8.07-2.809 0.64-5.609-1.12-6.249-3.93-0.643-2.81 1.11-5.61 3.926-6.25 31.9-7.291 59.263-4.15 81.337 9.34 2.46 1.51 3.24 4.72 1.73 7.18zm10.25-22.805c-1.89 3.075-5.91 4.045-8.98 2.155-22.51-13.839-56.823-17.846-83.448-9.764-3.453 1.043-7.1-0.903-8.148-4.35-1.04-3.453 0.907-7.093 4.354-8.143 30.413-9.228 68.222-4.758 94.072 11.127 3.07 1.89 4.04 5.91 2.15 8.976v-0.001zm0.88-23.744c-26.99-16.031-71.52-17.505-97.289-9.684-4.138 1.255-8.514-1.081-9.768-5.219-1.254-4.14 1.08-8.513 5.221-9.771 29.581-8.98 78.756-7.245 109.83 11.202 3.73 2.209 4.95 7.016 2.74 10.733-2.2 3.722-7.02 4.949-10.73 2.739z"></path>
                </svg>

            </a>
        </div>
        <div>
            <ul>
                <li v-for="play in plays">
                    {{play.format("dddd DD. MMMM: HH:mm:ss")}}
                </li>
            </ul>
        </div>
        <router-link class="closeButton" :to="{ name: 'List', params: { channel: $route.params.channel }}" replace
                     :style="{color: color.backgroundColor}">
            &times;
        </router-link>
    </div>
</template>

<script>
    import axios from "axios";
    import moment from "moment";
    import "moment/locale/de-at";

    if (import.meta.env.NODE_ENV === "production") {
        axios.defaults.headers.common['X-Requested-With'] = "XMLHttpRequest";
    }

    const baseURL = "/api/";

    export default {
        name: "detailview",
        data() {
            return {
                plays: [],
            };
        },
        props: ['songs', 'color', 'momentDate', 'dateType'],
        mounted() {
            this.getPlays();
            document.title = "Radiostats - " + this.song.song.title + " - " + this.song.song.artist;
        },
        methods: {
            getPlays: function() {
                let vm = this;
                this.plays = [];
                axios.get(baseURL + this.$route.params.channel + "/plays/" + this.$route.params.songId, {
                    params: {
                        date: vm.momentDate.format("YYYY-MM-DD"),
                        dateType: vm.dateType
                    }
                })
                    .then(function(response) {
                        response.data.forEach(function(time) {
                            vm.plays.push(moment(time));
                        });
                        // document.title = "Radiostats - " + vm.channels[vm.channel].stationname;

                    })
                    .catch(function(error) {
                        vm.httpError = error;
                    });
            },
        },
        computed: {
            song() {
                return this.songs[this.$route.params.songId];
            },
        },
        components: {},
        watch: {
            song: function() {
                this.getPlays();
                document.title = "Radiostats - " + this.song.song.title + " - " + this.song.song.artist;
            },
        }
    };
</script>

<style lang="scss">
    @import "./variables";

    .detailWrapper {
        padding: 0;
    }

    .detailView {
        position: relative;
        background-color: #f5f5f5;

        img, .imgPlaceholder {
            width: 250px;
            height: 250px;
            background-color: #eee;
            display: block;

            div {
                text-align: center;
                vertical-align: middle;
                line-height: 250px;
                font-size: 90px;
                font-weight: bold;
            }
        }

        > div {
            padding: 15px 15px !important;
        }

        audio {
            width: 250px;
        }

        .spotifyLink {
            display: inline-block;
            width: 250px;
            margin-top: 5px;

            &:hover {
                color: #1ED760 !important;
            }

            svg {
                fill: currentColor;
                display: block;
                width: 50px;
                height: 50px;
                margin-left: 100px;
            }
        }

        ul {
            max-height: 250px;
            overflow-y: auto;
            -webkit-overflow-scrolling: touch;
            list-style: none;
        }

        .closeButton {
            position: absolute;
            font-size: 40px;
            line-height: 10px;
            top: 10px;
            right: 20px;
            padding: 10px;
            cursor: pointer;
            transition: color 0.2s;

            &:hover {
                color: darkgrey !important;
            }

        }
    }

</style>

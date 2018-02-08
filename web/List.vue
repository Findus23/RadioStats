<template>
    <div id="list">
        <div id="channelSelector">
            <router-link v-for="channel in channels" :key="channel.shortname"
                         :to="{ name: 'List', params: { channel: channel.shortname }}">
                <img :src="require('./icons/'+icon(channel.shortname))"
                     :alt="channel.stationname" :title="channel.stationname"
                     :class="channel.has_data?[]:['noData']">

            </router-link>
            <!--
            <audio controls>
                <source :src="channel.streamurl +';'" type="audio/mpeg">
            </audio>
            -->
        </div>
        <header v-if="channelData"
                :style="{backgroundColor:channelData.primary_color,color:channelData.secondary_color}">
            <h2 v-if="channelData">{{channelData.stationname}}</h2>

        </header>
        <main>
            <table>
                <tr v-for="song in popular">
                    <td>{{song.song.title}}</td>
                    <td>{{song.song.artist}}</td>
                    <td>{{song.count}}</td>
                </tr>
            </table>
            <div id="loadMore" role="button" v-on:click="getAdditional" v-if="showMore &&channelData">
                Mehr anzeigen
            </div>
            <div id="httpError" v-if="httpError" class="message">
                <strong>Beim Laden ist ein Fehler aufgetreten:</strong> {{httpError.message}}
            </div>
            <div id="noData" class="message" v-if="(!channelData||!channelData.has_data)&&!httpError">
                <strong>Keine Daten!</strong> Leider gibt es für diesen Sender noch keine Daten.
            </div>
        </main>
    </div>
</template>

<script>
    import axios from "axios";

    export default {
        components: {},
        name: 'list',
        data() {
            return {
                channels: [],
                popular: [],
                offset: 0,
                showMore: true,
                httpError: false
            };
        },
        props: ["channel"],
        computed: {
            channelData: function() {
                return this.channels[this.channel];
            }
        },
        methods: {
            getChannels: function() {
                let vm = this;
                axios.get('http://127.0.0.1:5001/', {
                    params: {}
                })
                    .then(function(response) {
                        vm.channels = response.data;
                        vm.getPopular();
                    })
                    .catch(function(error) {
                        vm.httpError = error;
                    });
            },
            getPopular: function() {
                if (!this.channelData || !this.channelData.has_data) {
                    this.popular = [];
                    return false;
                }
                let vm = this;
                axios.get('http://127.0.0.1:5001/' + this.channel, {
                    params: {}
                })
                    .then(function(response) {
                        vm.offset += 5;
                        vm.popular = response.data;
                    })
                    .catch(function(error) {
                        vm.httpError = error;
                    });
            },
            getAdditional: function() {
                let vm = this;

                axios.get('http://127.0.0.1:5001/' + this.channel, {
                    params: {
                        offset: vm.offset
                    }
                })
                    .then(function(response) {
                        vm.offset += 5;
                        vm.popular = vm.popular.concat(response.data);
                        if (response.data.length < 5) {
                            vm.showMore = false
                        }
                    })
                    .catch(function(error) {
                        vm.httpError = error;
                    });

            },
            icon: function(id) {
                if (id === "fm4" || id === "oe3") {
                    return id + ".svg";
                } else {
                    return id + ".png";
                }
            }

        },
        watch: {
            channel: function(id) {
                this.offset = 0;
                this.showMore = true;
                this.httpError = false;

                this.getPopular()
            }
        },
        mounted: function() {
            this.getChannels();
        }
    };
</script>

<style lang="scss">
    @import "variables";
    @import "node_modules/milligram/src/Color";
    @import "node_modules/milligram/src/Utility";

    body {
        background-color: #ffffff;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='5' height='5'%3E%3Crect width='2.5' height='5' fill='white' /%3E%3Crect x='2.5' y='0' width='2.5' height='5' fill='%23f5f5f5' /%3E%3C/svg%3E");
        font-family: -apple-system, "Helvetica Neue Light", "HelveticaNeue", "Helvetica Neue", "Roboto", "Liberation Sans", Arial, sans-serif;
        color: #212121;
    }

    header {
        padding: 2.5rem;
        transition: color .2s, background-color .2s;
        h2 {
            font-weight: bold;
            text-align: center;
            margin: 0;
        }
    }

    main {
        background-color: white;
        padding: 2rem;
    }

    #channelSelector {
        margin: 16px 0;
        display: flex;
        justify-content: space-around;
        a {
            display: block;
            img {
                display: block;
                width: 40px;
                height: 40px;
                transition: filter .2s;
                &.noData:not(:hover) {
                    filter: grayscale(0.7);
                }
            }
        }
    }

    table {
        margin: 0;
    }

    #loadMore {
        padding: 10px 0;
        width: 100%;
        text-align: center;
        cursor: pointer;
        transition: background-color .2s;
        &:hover {
            background-color: #eee;
        }
    }

    .message {
        width: 100%;
        padding: 10px;
        background-color: #eee;
    }

    #httpError {
        background-color: $warning;
    }

</style>

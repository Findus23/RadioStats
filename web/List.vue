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
            <div id="date" class="row">
                <div class="column">
                    <datepicker language="de" v-model="date" :mondayFirst="true" :inline="true"
                                :highlighted="highlighted"></datepicker>

                </div>
                <div class="column">

                    <input type="radio" id="day" value="day" v-model="dateType">
                    <label class="label-inline" for="day">Tag</label>
                    <br>
                    <input type="radio" id="week" value="week" v-model="dateType">
                    <label class="label-inline" for="week">Woche</label>
                    <br>
                    <input type="radio" id="month" value="month" v-model="dateType">
                    <label class="label-inline" for="month">Monat</label>
                    <br>
                    <input type="radio" id="alltime" value="alltime" v-model="dateType">
                    <label class="label-inline" for="alltime">Gesamter Zeitraum</label>
                </div>
            </div>
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
    import Datepicker from 'vuejs-datepicker';

    const baseURL = (process.env.NODE_ENV === "production") ? "/api/" : "http://127.0.0.1:5000/api/";

    export default {
        components: {Datepicker},
        name: 'list',
        data() {
            return {
                channels: [],
                popular: [],
                offset: 0,
                showMore: true,
                httpError: false,
                date: new Date(),
                dateType: "week",
                highlighted: {
                    from: new Date(),
                    to: new Date(),
                }
            };
        },
        props: ["channel"],
        computed: {
            channelData: function () {
                return this.channels[this.channel];
            }
        },
        methods: {
            getChannels: function () {
                let vm = this;
                axios.get(baseURL, {
                    params: {}
                })
                    .then(function (response) {
                        vm.channels = response.data;
                        vm.getPopular();
                    })
                    .catch(function (error) {
                        vm.httpError = error;
                    });
            },
            getPopular: function () {
                this.offset = 0;
                this.showMore = true;
                this.httpError = false;

                if (!this.channelData || !this.channelData.has_data) {
                    this.popular = [];
                    return false;
                }
                let vm = this;
                axios.get(baseURL + this.channel, {
                    params: {
                        date: vm.date.toISOString().split('T')[0],
                        dateType: vm.dateType
                    }
                })
                    .then(function (response) {
                        vm.offset += 5;
                        vm.popular = response.data;
                    })
                    .catch(function (error) {
                        vm.httpError = error;
                    });
            },
            getAdditional: function () {
                let vm = this;

                axios.get(baseURL + this.channel, {
                    params: {
                        offset: vm.offset,
                        date: vm.date.toISOString().split('T')[0],
                        dateType: vm.dateType
                    }
                })
                    .then(function (response) {
                        vm.offset += 5;
                        vm.popular = vm.popular.concat(response.data);
                        if (response.data.length < 5) {
                            vm.showMore = false;
                        }
                    })
                    .catch(function (error) {
                        vm.httpError = error;
                    });

            },
            icon: function (id) {
                if (id === "fm4" || id === "oe3") {
                    return id + ".svg";
                } else {
                    return id + ".png";
                }
            },
            updateSelection: function () {
                let from, to;
                let y = this.date.getFullYear();
                let d = this.date.getDay();
                let m = this.date.getMonth();
                switch (this.dateType) {
                    case "day":
                        from = new Date(this.date);
                        to = new Date(this.date);
                        break;
                    case "week":
                        let diff = this.date.getDate() - (d - 1) + (d === 0 ? -7 : 0);
                        from = new Date(this.date);
                        from.setDate(diff);
                        to = new Date(this.date);
                        to.setDate(diff + 6);
                        break;
                    case "month":
                        from = new Date(y, m, 1);
                        to = new Date(y, m + 1, 1);
                        break;
                    default:
                        from = new Date(2000, 0, 0);
                        to = new Date(2050, 0, 0);
                }
                from.setHours(0, 0, 0, 0);
                to.setHours(23, 59, 59, 0);
                this.highlighted = {
                    "from": from,
                    "to": to,
                };
            }
        },
        watch: {
            channel: function () {
                this.getPopular();
            },
            dateType: function () {
                this.updateSelection();
                this.getPopular();
            },
            date: function () {
                this.updateSelection();
                this.getPopular();
            }

        },
        mounted: function () {
            this.getChannels();
            this.updateSelection();
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

    #date {
        align-items: center;
        .vdp-datepicker__calendar {
            margin-right: 0;
            margin-left: auto;
        }
    }

</style>

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
            <div role="button" tabindex="0" v-on:click="toogleVisibility" v-on:keyup.enter="toogleVisibility">
                Meistgespielte Lieder {{formatDate()}}
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 560" :class="showDate?[]:['disabled']">
                    <path d="M480 344.181L268.869 131.889c-15.756-15.859-41.3-15.859-57.054 0-15.754 15.857-15.754 41.57 0 57.431l237.632 238.937c8.395 8.451 19.562 12.254 30.553 11.698 10.993.556 22.159-3.247 30.555-11.698L748.186 189.32c15.756-15.86 15.756-41.571 0-57.431s-41.299-15.859-57.051 0L480 344.181z"></path>
                </svg>
            </div>
        </header>
        <transition name="expand">
            <div id="date" v-if="showDate">
                <div>
                    <datepicker language="de" v-model="date" :mondayFirst="true" :inline="true"
                                :highlighted="highlighted"></datepicker>

                </div>
                <div>
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
        </transition>
        <main>
            <table>
                <tr v-for="song in popular">
                    <td>{{song.song.title}}</td>
                    <td>{{song.song.artist}}</td>
                    <td>{{song.count}}</td>
                </tr>
            </table>
            <div id="loadMore" role="button" tabindex="0" v-on:click="getAdditional" v-on:keyup.enter="getAdditional"
                 v-if="showMore &&channelData">
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
    import moment from "moment";
    import "moment/locale/de-at";
    import Datepicker from 'vuejs-datepicker';

    if (process.env.NODE_ENV === "production") {
        axios.defaults.headers.common['X-Requested-With'] = "XMLHttpRequest";
    }

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
                },
                showDate: false
            };
        },
        props: ["channel"],
        computed: {
            channelData: function () {
                return this.channels[this.channel];
            },
            momentDate: function () {
                return moment(this.date);
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
                        document.title = "Radiostats - " + vm.channels[vm.channel].stationname;
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
                        date: vm.momentDate.format("YYYY-MM-DD"),
                        dateType: vm.dateType
                    }
                })
                    .then(function (response) {
                        vm.offset += 5;
                        vm.popular = response.data;
                        if (response.data.length < 5) {
                            vm.showMore = false;
                        }

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
                        date: vm.momentDate.format("YYYY-MM-DD"),
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
                let date = moment(this.date);
                if (this.dateType !== "alltime") {
                    from = moment(date);
                    to = moment(date);
                    from.startOf(this.dateType);
                    to.endOf(this.dateType);
                } else {
                    from = moment("2000-01-01");
                    to = moment("2025-01-01");
                }
                this.highlighted = {
                    "from": from.toDate(),
                    "to": to.toDate(),
                };
            },
            formatDate: function () {
                switch (this.dateType) {
                    case "day":
                        return "am " + this.momentDate.format("D. MMMM");
                    case "week":
                        return "in der Woche des " + this.momentDate.format("D. MMMM");
                    case "month":
                        return "im " + this.momentDate.format("MMMM YYYY");
                    case "alltime":
                        return "im gesamten Zeitraum";
                }
            },
            toogleVisibility: function () {
                this.showDate = !this.showDate;
            }
        },
        watch: {
            channel: function () {
                document.title = "Radiostats - " + this.channelData.stationname;
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
        h2, div {
            font-weight: bold;
            text-align: center;
            margin: 0;
        }
        div {
            cursor: pointer;
            font-size: 3.0rem;
            line-height: 1.3;
            svg {
                width: 32px;
                height: 18.66px;
                transition: transform .3s;
                &.disabled {
                    transform: rotate(-90deg);

                }
            }
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
        @media screen and (max-width: 500px) {
            flex-wrap: wrap;
            a {
                margin: 10px 10px;
            }
        }
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
        background-color: #eee;
        align-items: center;
        .vdp-datepicker__calendar {
            margin-right: 0;
            margin-left: auto;
        }
        display: flex;
        flex-direction: row;
        > div {
            width: 50%;
            padding: 0 15px;
        }
        @media (max-width: 700px) {
            flex-direction: column;
            > div {
                .vdp-datepicker {
                    margin: 0 auto;

                }
                width: 100%;
                padding: 15px 0 15px 15px;
            }
        }
    }

    .expand-enter-active, .expand-leave-active {
        transition: max-height .3s;

        max-height: 307px;
        overflow: hidden;
    }

    .expand-enter, .expand-leave-to {

        max-height: 0;
    }

</style>

<template>
    <div id="list">
        <div id="channelSelector">
            <router-link v-for="channel in channels" :key="channel.shortname"
                         :to="{ name: 'List', params: { channel: channel.shortname }}"
                         :style="{borderColor:channel.primary_color}">
                <img :src="icon(channel.shortname)"
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
            <h2 v-if="channelData">{{ channelData.stationname }}</h2>
            <div role="button" tabindex="0" v-on:click="toogleVisibility" v-on:keyup.enter="toogleVisibility">
                Meistgespielte Lieder {{ formatDate() }}
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 560" :class="showDate?[]:['disabled']">
                    <path d="M480 344.181L268.869 131.889c-15.756-15.859-41.3-15.859-57.054 0-15.754 15.857-15.754 41.57 0 57.431l237.632 238.937c8.395 8.451 19.562 12.254 30.553 11.698 10.993.556 22.159-3.247 30.555-11.698L748.186 189.32c15.756-15.86 15.756-41.571 0-57.431s-41.299-15.859-57.051 0L480 344.181z"></path>
                </svg>
            </div>
        </header>
        <transition name="expand">
            <div id="date" class="customRow" v-if="showDate">
                <div>
                    <datepicker :language="locale" v-model="date"  :inline="true"
                                :highlighted="highlighted"></datepicker>

                    <div v-if="showMore" v-on:click="getMany" class="getMany">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 8 8">
                            <path d="M3 0v3h-2l3 3 3-3h-2v-3h-2zm-3 7v1h8v-1h-8z"></path>
                        </svg>
                    </div>

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
            <div id="httpError" v-if="httpError" class="message">
                <strong>Beim Laden ist ein Fehler aufgetreten:</strong> {{ httpError.message }}
            </div>
            <div id="noData" class="message" v-if="(!channelData||!channelData.has_data)&&!httpError">
                <strong>Keine Daten!</strong> Leider gibt es für diesen Sender noch keine Daten.
            </div>
            <table>
                <template v-for="song in popular">
                    <tr v-on:click="toogleDetails($event,song.song.id)" class="clickable">
                        <td>
                            <img v-if="song.song.image_small" :src="song.song.image_small">
                            <div v-else class="imgPlaceholder"></div>
                        </td>
                        <td>
                            {{ song.song.title }}
                            <router-link :to="{ name: 'DetailView',params:{channel:channel, songId:song.song.id} }"
                                         replace style="display: none;">{{ song.song.title }}
                            </router-link>
                        </td>
                        <td>{{ song.song.artist }}</td>
                        <td>{{ song.count }}</td>
                    </tr>
                    <tr v-if="parseInt($route.params.songId) === song.song.id">
                        <td colspan="4" class="detailWrapper">
                            <router-view :songs="songs"
                                         :color="{backgroundColor:channelData.primary_color,color:channelData.secondary_color}"
                                         :momentDate="momentDate" :dateType="dateType"></router-view>
                        </td>
                    </tr>
                </template>
            </table>
            <div id="loadMore" role="button" tabindex="0" v-on:click="getAdditional" v-on:keyup.enter="getAdditional"
                 v-if="showMore &&channelData&&channelData.has_data">
                Mehr anzeigen
            </div>
        </main>

        <info v-if="channelData"
              :color="{backgroundColor:channelData.primary_color,color:channelData.secondary_color}"></info>
    </div>
</template>

<script>
import axios from "axios";
import moment from "moment";
import "moment/locale/de-at";
import Datepicker from 'vue3-datepicker';
import { deAT } from 'date-fns/locale'
import Info from "./Info.vue";
import {icon} from "./utils";

if (import.meta.env.PROD) {
    axios.defaults.headers.common['X-Requested-With'] = "XMLHttpRequest";
}

const baseURL = "/api/";

export default {
    components: {Datepicker, Info},
    name: 'list',
    data() {
        return {
            channels: [],
            songs: [],
            offset: 0,
            showMore: true,
            httpError: false,
            date: new Date(),
            dateType: "week",
            highlighted: {
                from: new Date(),
                to: new Date(),
            },
            showDate: false,
            locale: deAT
        };
    },
    props: ["channel"],
    computed: {
        channelData: function () {
            return this.channels[this.channel];
        },
        momentDate: function () {
            return moment(this.date);
        },
        popular: function () {
            function compare(a, b) {
                if (a.order < b.order)
                    return -1;
                if (a.order > b.order)
                    return 1;
                return 0;
            }

            let songArray = Object.values(this.songs);
            return songArray.sort(compare);
        }

    },
    methods: {
        getChannels: function () {
            axios.get(baseURL, {
                params: {}
            })
                .then(response => {
                    const all = response.data["all"];
                    this.channels = response.data;
                    delete response.data["all"];
                    response.data["all"] = all;
                    document.title = "Radiostats - " + this.channels[this.channel].stationname;
                    this.getPopular();

                })
                .catch(error => {
                    this.httpError = error;
                });
        },
        getPopular: function () {
            this.offset = 0;
            this.showMore = true;
            this.httpError = false;

            if (!this.channelData || !this.channelData.has_data) {
                this.songs = [];
                return false;
            }
            axios.get(baseURL + this.channel, {
                params: {
                    date: this.momentDate.format("YYYY-MM-DD"),
                    dateType: this.dateType
                }
            })
                .then(response => {
                    this.offset += 10;
                    this.songs = response.data;
                    if (Object.keys(response.data).length < 10) {
                        this.showMore = false;
                    }
                    let urlsongID = parseInt(this.$route.params.songId);
                    if (urlsongID && typeof this.songs[urlsongID] === "undefined") {
                        axios.get(baseURL + this.channel + "/details/" + urlsongID, {
                            params: {
                                date: this.momentDate.format("YYYY-MM-DD"),
                                dateType: this.dateType
                            }
                        })
                            .then(response => {
                              this.songs[urlsongID] = response.data
                                // this.$set(this.songs, urlsongID, response.data);
                            });

                        console.log("Song not in view: " + urlsongID);
                    }

                })
                .catch(error => {
                    this.httpError = error;
                });
        },
        getAdditional: function (many) {
            const loadNumber = (many === true) ? 1000 : 10;
            axios.get(baseURL + this.channel, {
                params: {
                    offset: this.offset,
                    date: this.momentDate.format("YYYY-MM-DD"),
                    dateType: this.dateType,
                    highlimit: many === true
                }
            })
                .then(response => {
                    this.offset += loadNumber;
                    this.songs = Object.assign({}, this.songs, response.data);
                    if (Object.keys(response.data).length < loadNumber) {
                        this.showMore = false;
                    }
                })
                .catch(error => {
                    this.httpError = error;
                });

        },
        getMany: function () {
            this.getAdditional(true)
        },
        icon(id) {
            return icon(id)
        },
        iconFile: function (id) {
            if (id === "fm4" || id === "oe3" || id === "kht") {
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
        },
        toogleDetails: function ($event, songId) {
            if (this.$route.name !== "DetailView" || this.$route.params.songId !== songId) {
                this.$router.replace({name: 'DetailView', params: {channel: this.channel, songId: songId}});
            } else {
                this.$router.replace({name: 'List', params: {channel: this.channel}});
            }
        }
    },
    watch: {
        channel: function () {
            // document.title = "Radiostats - " + this.channelData.stationname;
            this.getPopular();
        },
        '$route.name': function (id) {
            document.title = "Radiostats - " + this.channelData.stationname;
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
@import "./variables";
@import "./node_modules/milligram/src/Color";
@import "./node_modules/milligram/src/Utility";

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
      fill: currentColor;
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
    /*border-bottom: solid 5px;*/

    &.router-link-active {
      border-bottom: solid 5px;
    }

    display: block;

    img {
      margin-bottom: 5px;
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

  img, .imgPlaceholder {
    width: 36px;
    height: 36px;
    background-color: #eee;
    display: block;
  }

  tr.clickable {
    cursor: pointer;
  }
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
  background-color: #f0ad4e;
}

#date {
  .vdp-datepicker__calendar {
    margin-right: 0;
    margin-left: auto;
  }

  @media (max-width: 700px) {
    > div {
      .vdp-datepicker {
        margin: 0 auto;

      }
    }
  }
}

.customRow {
  background-color: #eee;
  display: flex;
  flex-direction: row;
  align-items: center;

  > div {
    width: 50%;
    padding: 0 15px !important;
  }

  @media (max-width: 700px) {
    flex-direction: column;
    > div {
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

.getMany {
  max-width: 300px;
  margin-left: auto;

  svg {
    display: block;
    margin: 10px auto;
  }
}

</style>

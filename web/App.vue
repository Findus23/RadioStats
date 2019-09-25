<template>
    <div id="app" class="container">
        <div class="iewarning" v-if="isIE">
            <p>Achtung: Sie verwenden Internet Explorer, ein Webbrowser, der seit vielen Jahren nicht mehr
                weiterentwickelt wird und bei dem regelmäßig schwere Sicherheitslücken gefunden werden!</p>
            <p>Erst im September 2019 wurde eine Sicherheitslücke gefunden, die jeder Webseite erlaubt, komplett auf den
                PC zuzugreifen.<a
                        href="https://www.heise.de/security/meldung/Notfallpatch-Attacken-gegen-Internet-Explorer-4537525.html">
                    (mehr Informationen)
                </a>
            </p>
            <p>
                Es wird daher dringend empfohlen auf einen anderen Webbrowser, der aktiv gewartet wird (wie zum Beispiel
                <a href="https://www.mozilla.org/de/firefox/new/">Firefox</a>), umzusteigen.
                <a href="https://techcommunity.microsoft.com/t5/Windows-IT-Pro-Blog/The-perils-of-using-Internet-Explorer-as-your-default-browser/ba-p/331732"
                   target="_blank" rel="noopener">
                    Selbst Microsoft
                </a>
                empfielt dringend stattdessen ihren neuen Browser "Edge" zu verwenden.
            </p>
        </div>
        <router-view></router-view>
    </div>
</template>

<script>
    export default {
        name: 'app',
        props: ["language"],
        computed: {
            isIE() {
				let ua = window.navigator.userAgent;
				return /MSIE|Trident/.test(ua);
            }
        }
    };
</script>

<style lang="css" src="./node_modules/normalize.css/normalize.css">
</style>

<style lang="scss">
    @import "variables";
    @import "node_modules/milligram/src/milligram";

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

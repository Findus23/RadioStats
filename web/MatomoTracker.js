var MatomoTracker = /** @class */ (function () {
    function MatomoTracker() {
    }
    MatomoTracker.prototype.init = function () {
        // @ts-ignore
        if (typeof _paq === 'undefined') { // should only occur with hot reloading
            // @ts-ignore
            var _paq_1 = _paq_1 || [];
            _paq_1.push(['enableHeartBeatTimer']);
            if (process.env.NODE_ENV === "production") {
                _paq_1.push(["setDoNotTrack", true]);
            }
            (function () {
                var u = (process.env.NODE_ENV === "production") ? "https://matomo.lw1.at/" : "//localhost/piwik/";
                _paq_1.push(['setTrackerUrl', u + 'piwik.php']);
                _paq_1.push(['setSiteId', (process.env.NODE_ENV === "production") ? 15 : 6]);
                var d = document, g = d.createElement('script'), s = d.getElementsByTagName('script')[0];
                g.type = 'text/javascript';
                g.async = true;
                g.defer = true;
                g.src = u + 'piwik.js';
                // @ts-ignore
                s.parentNode.insertBefore(g, s);
            })();
            // @ts-ignore
            window._paq = _paq_1;
        }
        else {
            console.info("Piwik already initialized");
        }
    };
    return MatomoTracker;
}());
export default MatomoTracker;

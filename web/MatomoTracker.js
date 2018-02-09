export default class MatomoTracker {
    init() {
        if (typeof _paq === 'undefined') { // should only occur with hot reloading
            let _paq = _paq || [];
            _paq.push(['enableHeartBeatTimer']);
            if (process.env.NODE_ENV === "production") {
                _paq.push(["setDoNotTrack", true]);
            }
            (function() {
                let u = (process.env.NODE_ENV === "production") ? "https://matomo.lw1.at/" : "//localhost/piwik/";
                _paq.push(['setTrackerUrl', u + 'piwik.php']);
                _paq.push(['setSiteId', (process.env.NODE_ENV === "production") ? 15 : 5]);
                let d = document, g = d.createElement('script'), s = d.getElementsByTagName('script')[0];
                g.type = 'text/javascript';
                g.async = true;
                g.defer = true;
                g.src = u + 'piwik.js';
                s.parentNode.insertBefore(g, s);
            })();
            window._paq = _paq;
        } else {
            console.info("Piwik already initialized");
        }
    }
}

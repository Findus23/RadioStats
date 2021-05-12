export default class MatomoTracker {
    init() {
        if (typeof _paq === 'undefined') { // should only occur with hot reloading
            var _paq = window._paq = window._paq || [];            _paq.push(['disableCookies']);
            _paq.push(['enableHeartBeatTimer']);
            if (import.meta.env.NODE_ENV === "production") {
                _paq.push(["setDoNotTrack", true]);
            }
            (function() {
                let u ="https://matomo.lw1.at/" ;
                _paq.push(['setTrackerUrl', u + 'piwik.php']);
                _paq.push(['setSiteId', (import.meta.env.NODE_ENV === "production") ? 15 : 6]);
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

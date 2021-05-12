const httpProxy = require('http-proxy');
const proxy = httpProxy.createProxyServer({
    target: 'http://localhost:5000',
    timeout: 30 * 1000
});

/** @type {import("snowpack").SnowpackUserConfig } */
module.exports = {
    mount: {
        public: {url: '/', static: true},
        "src/icons": {url: "/icons/", static: true},
        src: {url: '/dist'},
    },
    routes: [
        /* Enable an SPA Fallback in development: */
        {
            src: '/api/.*',
            dest: (req, res) => {
                proxy.web(req, res, e => console.log(e));
            },
        },
        {"match": "routes", "src": ".*", "dest": "/index.html"},
    ],
    plugins: [
        "./workaroundPlugin",
        "@morgul/snowpack-plugin-vue2",
        '@snowpack/plugin-sass',
        [
            'snowpack-plugin-replace',
            {
                list: [
                    {
                        from: 'process.env.NODE_ENV',
                        to: JSON.stringify('production')
                    },
                ],
            }
        ],
    ],
    optimize: {
        /* Example: Bundle your final build: */
        bundle: true,
        minify: true,
        target: "es2018"
    },
    devOptions: {
        open: "none"
    }
}

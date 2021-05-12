module.exports = function config() {
    return {
        name: 'snowpack-config-resolveProxyImports-plugin',
        config(config) {
            setTimeout(() => {
                config.buildOptions.resolveProxyImports = true
            })
        },
    };
}

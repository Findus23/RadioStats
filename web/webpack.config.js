let path = require('path');
let webpack = require('webpack');
let CleanWebpackPlugin = require('clean-webpack-plugin');
let HtmlWebpackPlugin = require('html-webpack-plugin');
let SriPlugin = require('webpack-subresource-integrity');
let CompressionPlugin = require('compression-webpack-plugin');
let ExtractTextPlugin = require("extract-text-webpack-plugin");

module.exports = {
    entry: {polyfill: "@babel/polyfill", app: './main.js'},
    output: {
        path: path.resolve(__dirname, '../dist'),
        publicPath: '/',
        filename: '[name]-build-[hash].js',
        crossOriginLoading: "anonymous"
    },
    module: {
        rules: [
            {
                test: /\.vue$/,
                loader: 'vue-loader',
                options: {
                    sourceMap: true,
                    extractCSS: process.env.NODE_ENV === 'production',
                    cssSourceMap: true,
                    transformToRequire: {
                        video: ['src', 'poster'],
                        source: 'src',
                        img: 'src',
                        image: 'xlink:href'
                    },
                    postcss: [require('autoprefixer')()]
                }
            },
            {
                test: /\.js$/,
                exclude: /(node_modules|bower_components)/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: [
                            [
                                "@babel/preset-env",
                                {
                                    "targets": {
                                        "browsers": [
                                            ">1% in AT"
                                        ]
                                    }
                                }
                            ]
                        ]
                    }
                }
            },
            {
                test: /\.(png|jpg|gif|svg)$/,
                use: [
                    {
                        loader: 'file-loader',
                        options: {
                            name: '[name].[ext]?hash=[hash]'
                        }
                    },
                    {
                        loader: 'image-webpack-loader',
                        options: {
                            bypassOnDebug: true,
                            mozjpeg: {
                                enabled: false
                            },
                        },
                    },
                ],
            }
        ]
    },
    devServer: {
        historyApiFallback: true,
        noInfo: true,
        overlay: true
    },
    performance: {
        hints: false
    },
    devtool: 'source-map',
    plugins: [
        new HtmlWebpackPlugin({
            title: 'My App',
            template: 'my-index.ejs',
            devServer: process.env.NODE_ENV === 'production' ? '' : 'http://localhost:8081',
        }),
        new webpack.NamedModulesPlugin(),
        new SriPlugin({
            hashFuncNames: ['sha256'],
            enabled: process.env.NODE_ENV === 'production',
        }),
        new webpack.optimize.CommonsChunkPlugin({name: "commons"}),
        new webpack.ContextReplacementPlugin(/moment[\/\\]locale$/, /de|en/)
    ]
};

if (process.env.NODE_ENV === 'production') {
    module.exports.devtool = '#source-map';
    // http://vue-loader.vuejs.org/en/workflow/production.html
    module.exports.plugins = (module.exports.plugins || []).concat([
        new CleanWebpackPlugin("dist"),
        new webpack.HashedModuleIdsPlugin({
            hashFunction: 'sha256',
            hashDigest: 'hex',
            hashDigestLength: 20
        }),
        new webpack.DefinePlugin({
            'process.env': {
                NODE_ENV: '"production"'
            }
        }),
        new webpack.optimize.UglifyJsPlugin({
            sourceMap: true,
            compress: {
                warnings: false
            }
        }),
        new webpack.LoaderOptionsPlugin({
            minimize: true
        }),
        new ExtractTextPlugin("style-[hash].css"),
        new CompressionPlugin({
            test: /\.(js|css)/
        }),
    ]);
}

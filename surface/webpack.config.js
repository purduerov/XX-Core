var webpack = require('webpack');
var ExtractTextPlugin = require('extract-text-webpack-plugin');
var combineLoaders = require('webpack-combine-loaders');
var path = require('path');

var BUILD_DIR = path.resolve(__dirname, 'frontend/src/elec_finals/');
var APP_DIR = __dirname;

var config = {
    entry: APP_DIR + '/frontend/index.jsx',
    output: {
        path: BUILD_DIR,
        filename: '.build.js'
    },
    plugins: [
        new ExtractTextPlugin(BUILD_DIR + '.styles.css'),
    ],
    module: {
        loaders: [{
            test: /\.jsx?$/,
            include: APP_DIR,
            loader: 'babel-loader',
            exclude: /node_modules/
        }, {
            test: /\.css$/,
            loader: combineLoaders([{
                loader: 'style-loader'
            }, {
                loader: 'css-loader',
                query: {
                    modules: true,
                    localIdentName: '[name]__[local]___[hash:base64:5]'
                }
            }])
        }],
    }
};

module.exports = config;
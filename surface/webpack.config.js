var webpack = require('webpack');
var ExtractTextPlugin = require('extract-text-webpack-plugin');
var combineLoaders = require('webpack-combine-loaders');
var path = require('path');

var BUILD_DIR = path.resolve(__dirname, 'frontend/src/elec_finals/');
var APP_DIR = __dirname;

/*
    https://github.com/webpack/webpack/issues/1189
    For those looking to understand how we get multiple file outputs, you're not able to directly specify different output files it seems.
    The original `entry: "/frontend/index.jsx"` was shorthand for writing the object that entry accepts.
    Writing out the full version, and taking advantage of webpack's [name] convention work-around, we use the name in the name: value pair
    that the object uses, to make the object value's name the output file's name as well.
*/

var config = {
    entry: {
        '.build.js': APP_DIR + '/frontend/index.jsx',
        '.build2.js': APP_DIR + '/frontend/index2.jsx',
    },
    output: {
        path: BUILD_DIR,
        filename: '[name]'
    },
    plugins: [
        new ExtractTextPlugin(BUILD_DIR + '.styles.css'),
    ],
    module: {
        loaders: [{
            test: /\.jsx?$/,
            include: APP_DIR,
            loader: 'babel-loader',
            exclude: /node_modules/,
            query: {
                presets: ['react']
            }
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
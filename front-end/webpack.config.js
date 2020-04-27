var path = require("path")
var webpack = require('webpack')
var BundleTracker = require('webpack-bundle-tracker')

module.exports = {
  context: __dirname,

  entry: './src/index.js',

  output: {
    path: path.resolve('./build/static/'),
    filename: "[name]-[hash].js",
  },

  plugins: [
    new BundleTracker({ filename: '../webpack-stats.json' }),
  ],

  module: {
    rules: [
      { test: /\.js$/, loader: 'babel-loader', exclude: /node_modules/ },
      { test: /\.jsx$/, loader: 'babel-loader', exclude: /node_modules/ },
      { test: /\.css$/i, use: ['style-loader', 'css-loader'] },
    ],
  },

}

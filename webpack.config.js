const path = require('path')

const MiniCssExtractPlugin = require("mini-css-extract-plugin")
const ManifestRevisionPlugin = require('manifest-revision-webpack-plugin')
const UglifyJsPlugin = require('uglifyjs-webpack-plugin')
const webpack = require('webpack')

const rootAssetPath = './app/static'
const devMode = process.env.NODE_ENV !== 'production'

module.exports = (env, options) => {
    return {
      entry: {
          app: [
            path.resolve(__dirname, './app/templates/app.js')
          ],
          vender_css: [
            path.resolve(__dirname, './node_modules/bootstrap/dist/css/bootstrap.min.css')
          ]
      },
      output: {
        path: path.resolve(__dirname, './build/public'),
        publicPath: 'http://localhost:2992/assets/',
        filename: '[name].[chunkhash].js',
        chunkFilename: '[id].[chunkhash].js'
      },
      resolve: {
        extensions: ['.js', '.css']
      },
      devServer: {
       headers: { "Access-Control-Allow-Origin": "*" }
      },
      module: {
          rules: [
              {
                test: /\.(py|pyc|html)$/,
                loader: 'ignore-loader'
              },
              {
                test: /\.css$/i,
                use: [
                  devMode ? 'style-loader' : MiniCssExtractPlugin.loader,
                  'css-loader'
                ]
              },
              {
                test: /\.js$/i, use: 'babel-loader',
                exclude: /node_modules/
              },
              {
                test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/,
                loader: 'url-loader?limit=10000&mimetype=application/font-woff'
              },
              {
                test: /\.(ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/,
                loader: "file-loader"
              },
              {
                test: /\.(jpe?g|png|gif|otf)(\?v=[0-9]\.[0-9]\.[0-9])?$/i,
                use: [
                  {
                    loader: 'file-loader',
                    options: {
                      name (file) {
                        if (env === 'development') {
                          return '[path][name].[ext]'
                        }

                        return '[hash].[ext]'
                      },
                      outputPath: rootAssetPath + '/images'
                    }
                  }
                ]
              }
          ]
      },
      plugins: [
        new UglifyJsPlugin(),
        new MiniCssExtractPlugin({
          filename: "[name].[hash].css",
          chunkFilename: "[id].[hash].css"
        }),
        new ManifestRevisionPlugin(path.join('build', 'manifest.json'), {
          rootAssetPath: rootAssetPath,
          ignorePaths: ['/images']
        })
      ]
  }
}

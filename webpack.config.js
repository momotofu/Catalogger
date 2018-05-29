const path = require('path')

const MiniCssExtractPlugin = require("mini-css-extract-plugin")
const ManifestRevisionPlugin = require('manifest-revision-webpack-plugin')
const UglifyJsPlugin = require('uglifyjs-webpack-plugin')

const rootAssetPath = './app/static'
const devMode = process.env.NODE_ENV !== 'production'

module.exports = (env, options) => {
    return {
      entry: {
          app: [
            path.resolve(__dirname, 'app/templates/app.js')
          ],
          venders: [
            path.resolve(__dirname, 'node_modules/bootstrap/dist/css/bootstrap.min.css')
          ],
      },
      output: {
        path: path.resolve(__dirname, './app/build/public'),
          publicPath: 'http://localhost:2992/assets/',
          filename: '[name].[chunkhash].js',
          chunkFilename: '[id].[chunkhash].js'
      },
      resolve: {
          extensions: ['.js', '.css']
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
                test: /\.(jpe?g|png|gif|svg([\?]?.*))$/i,
                use: [
                  `file?context=${rootAssetPath}&name=[path][name].[hash].[ext]`,
                  'image?bypassOnDebug&optimizationLevel=7&interlaced=false'
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
        new ManifestRevisionPlugin(path.join('./app/build', 'manifest.json'), {
          rootAssetPath: './app/static'
        })
      ]
  }
}

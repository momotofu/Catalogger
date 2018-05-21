const path = require('path')

const MiniCssExtractPlugin = require("mini-css-extract-plugin")
const ManifestRevisionPlugin = require('manifest-revision-webpack-plugin')

const rootAssetPath = './app'
const devMode = process.env.NODE_ENV !== 'production'

module.exports = (env, options) => {
    return {
      mode: options.mode,
      entry: `${rootAssetPath}/index.js`,
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
                test: /\.js$/i, use: 'script-loader',
                exclude: /node_modules/
              },
              {
                test: /\.css$/i,
                use: [
                  devMode ? 'style-loader' : MiniCssExtractPlugin.loader,
                  'css-loader'
                ]
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
          new MiniCssExtractPlugin({
            filename: "[name].[hash].css",
            chunkFilename: "[id].[hash].css"
          }),
        new ManifestRevisionPlugin(path.join('./app/build', 'manifest.json'), {
              rootAssetPath: rootAssetPath,
              ignorePaths: ['/styles', '/scripts']
          })
      ]
  }
}

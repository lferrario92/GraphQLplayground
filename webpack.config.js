const VueLoaderPlugin = require('vue-loader/lib/plugin')

module.exports = {
	mode: 'development',
	module: {
		rules: [
			{
				test: /\.vue$/,
				use: 'vue-loader',
			},
			{
				test: /\.graphql$/,
				use: 'graphql-tag/loader',
			},
		],
	},
	output: {
		filename: 'index.js',
		path: __dirname + '/cookbook/static',
	},
	plugins: [
    new VueLoaderPlugin()
  ],
	devServer: {
		publicPath: '/static/',
		proxy: {
			'**': {
				target: 'http://localhost:8000',
				secure: false,
				changeOrigin: true,
			}
		}
	},
}
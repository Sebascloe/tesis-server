const express = require('express')
const config = require('./config.js')

const app = express()

app.set('port', config.app.port)

module.exports = app
require('lib/setup')

Spine = require('spine')

Canvas = require('controllers/canvas')

class App extends Spine.Controller
  constructor: ->
    super
    
    @canvas = new Canvas
    @append @canvas

module.exports = App
    
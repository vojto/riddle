Spine = require('spine')

class View extends Spine.Controller
  constructor: ->
    super
    @render()
  
  render: ->
    @html @template(@)

module.exports = View
Spine = require('spine')

class View extends Spine.Controller
  constructor: ->
    super
    console.log 'constructing view'
    @render()
  
  render: ->
    @html @template(@)

module.exports = View
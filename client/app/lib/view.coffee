Spine = require('spine')

class View extends Spine.Controller
  constructor: ->
    super
  
  render: ->
    @renderTemplate()
  
  renderTemplate: ->
    @html @template(@) if @template

module.exports = View
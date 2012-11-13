Spine = require('spine')

class Page extends Spine.Controller
  ###
  This class represents single page of the application. It provides
  means to reuse layout elements on pages.
  ###
  
  template: require('templates/pages/page')
  
  constructor: ->
    super
    @render()
  
  render: ->
    @html @template(@)

module.exports = Page
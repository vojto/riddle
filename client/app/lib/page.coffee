Spine = require('spine')

class Page extends Spine.Controller
  ###
  This class represents single page of the application. It provides
  means to reuse layout elements on pages.
  ###
  
  constructor: ->
    super
    @render()
  
  render: ->
    @el.addClass('page')
  
  willShow: ->
    ###
    Performs additional additional before the page can be shown to the user
    ###

module.exports = Page
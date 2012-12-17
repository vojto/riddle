Spine = require('spine')
LoginStatusView = require('views/login_status_view')

class Page extends Spine.Controller
  ###
  This class represents single page of the application. It provides
  means to reuse layout elements on pages.
  ###

  constructor: ->
    super
    @render()

  addLoginStatus: ->
    @loginStatus = new LoginStatusView
    @append @loginStatus

  addBackgroundLogo: ->
    @logo = $('<div />').addClass('background-logo')
    @append @logo

  render: ->
    @el.addClass('page')

  show: ->
    ###
    Performs additional additional before the page can be shown to the user
    ###

  setupHalfling: ->
    @$el.addClass('halfling')
    $(document.body).find('.halfling-close').remove()
    $halflingClose = $('<div />').addClass('halfling-close')
    $(document.body).append($halflingClose)
    $halflingClose.click =>
      history.go(-1)
      $halflingClose.hide()


module.exports = Page
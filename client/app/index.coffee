require('lib/setup')

Spine = require('spine')
Atmos = require('atmos2')

Modifiers = require('lib/modifiers')
Session = require('models/session')

if window.isProduction
  appBase = 'http://riddle.rinik.net'
else
  appBase = 'http://localhost:5000'


class App extends Spine.Controller
  className: 'app'

  @base: appBase

  constructor: ->
    super

    App.instance = @

    # Modifier keys interceptor
    Modifiers.setup()

    # Session
    @user = Session.user()

    # Networking
    @atmos = new Atmos(base: @constructor.base)
    @atmos.bind 'auth_fail', @didFailAuth
    @atmos.bind 'response_error', @didFailResponse

    # Teacher routes
    @addRoutesForPages
      '/login'                          : 'pages/teacher/login_page'
      '/registration'                   : 'pages/teacher/registration_page'
      '/dashboard'                      : 'pages/teacher/dashboard_page'
      '/categories/new'                 : 'pages/teacher/category_add_page'
      '/error'                          : 'pages/teacher/error_page'
      '/course/:id'                     : 'pages/teacher/course_page'
      '/course/:course_id/question/new' : 'pages/teacher/question_form_page'
      '/course/:course_id/question/:id/edit' : 'pages/teacher/question_form_page'
      '/course/:course_id/question/:id' : 'pages/teacher/question_page'
    defaultRoute = if @user then '/dashboard' else '/login'
    Spine.Route.add '/': => @navigate(defaultRoute)

    # Student routes
    @addRoutesForPages
      '/:course_id'                     : 'pages/student/course/show_page'
      '/student/login'                  : 'pages/student/login_page'

    # Special pages
    @bind 'willShowPage', @willShowPage

    Spine.Route.setup()

    # Views
    @setupLoaderView()
    @setupErrorView()

  willShowPage: (page) =>
    if page.constructor.name == 'CoursePage' and @user
      @showPageAtPath('pages/teacher/dashboard_page', {})


  ## Page routing
  #  To be refactored into a general class

  addRoutesForPages: (table) ->
    ### Table is in format route -> class path ###
    @pageTable or= {}
    $.extend(@pageTable, table)
    for routeName, path of table
      Spine.Route.add routeName, @didChangeRoute

  didChangeRoute: (match) =>
    input = match.match.input
    matchedRoute = null
    for route in Spine.Route.routes
      if route.route.exec(input)
        matchedRoute = route
        break

    pagePath = @pageTable[route.path]

    if !pagePath
      console.log 'Routing error: ', match

    @showPageAtPath(pagePath, match)

  showPageAtPath: (pagePath, match) ->
    @pageInstances or= {}
    pageClass = require(pagePath)

    if @pageInstances[pagePath]
      page = @pageInstances[pagePath]
    else
      page = @pageInstances[pagePath] = new pageClass

    if page
      @constructor.page = page # TODO: Come up with better way than global
      @trigger 'willShowPage', page
      page.show(match)
      # @el.children().detach()
      @append(page)

  didFailAuth: =>
    Session.logout()
    @navigate '/login'

  didFailResponse: =>
    Session.logout()
    @navigate '/error', shim: true

  ## Views

  setupLoaderView: ->
    @$loader = $('<div />').addClass('loader')
    @$loader.hide()
    @append @$loader

    @$loader.bind 'ajaxStart', ->
      $(@).show()
    @$loader.bind 'ajaxComplete', ->
      $(@).hide()

  ## Showing error

  setupErrorView: ->
    @$error = $('<div />').addClass('error-message').text('error here')
    @$error.hide()
    @append @$error

  @showError: (text) ->
    @instance.showError(text)

  showError: (text) ->
    @$error.text(text)
    @$error.gfx({rotate3d: "1,0,0,90deg"}, {duration: 0})
    @$error.show()
    @$error.gfx({rotate3d: "1,0,0,0deg"}, {duration: 250})
    setTimeout =>
      @$error.gfx({rotate3d: "1,0,0,90deg"}, {duration: 250, complete: =>
        @$error.hide()
      })
    , 3500


window.App = App
module.exports = App
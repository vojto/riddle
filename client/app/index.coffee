require('lib/setup')

Spine = require('spine')
Atmos = require('atmos2')

Modifiers = require('lib/modifiers')
Session = require('models/session')

LoginPage = require('pages/login_page')
DashboardPage = require('pages/dashboard_page')
CategoryAddPage = require('pages/category_add_page')

class App extends Spine.Controller
  className: 'app'

  @base: 'http://localhost:5000'

  constructor: ->
    super

    # Modifier keys interceptor
    Modifiers.setup()

    # Session
    user = Session.user()

    # Networking
    @atmos = new Atmos(base: @constructor.base)
    @atmos.bind 'auth_fail', @didFailAuth
    @atmos.bind 'response_error', @didFailResponse

    # Routing
    @addRoutesForPages
      '/login'          : 'pages/login_page'
      '/registration'   : 'pages/registration_page'
      '/dashboard'      : 'pages/dashboard_page'
      '/categories/new' : 'pages/category_add_page'
      '/error'          : 'pages/error_page'
      '/course/:id'     : 'pages/course_page'
      '/course/:course_id/question/new' : 'pages/question_form_page'
      '/course/:course_id/question/:id' : 'pages/question_form_page'

    defaultRoute = if user then '/dashboard' else '/login'
    Spine.Route.add '/': => @navigate(defaultRoute)
    Spine.Route.setup()

    # Views
    @setupLoaderView()

  addRoutesForPages: (table) ->
    ### Table is in format route -> class path ###
    @pageTable = table
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

    pageClass = require(pagePath)
    @pageInstances or= {}

    if @pageInstances[pagePath]
      page = @pageInstances[pagePath]
    else
      page = @pageInstances[pagePath] = new pageClass

    if page
      @constructor.page = page # TODO: Come up with better way than global
      page.show(match)
      # @el.children().detach()
      @append(page)

  didFailAuth: =>
    Session.logout()
    @navigate '/login'

  didFailResponse: =>
    Session.logout()
    @navigate '/error'

  # Views

  setupLoaderView: ->
    @$loader = $('<div />').addClass('loader')
    @$loader.hide()
    @append @$loader

    @$loader.bind 'ajaxStart', ->
      $(@).show()
    @$loader.bind 'ajaxComplete', ->
      $(@).hide()

window.App = App
module.exports = App
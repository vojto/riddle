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
  
  constructor: ->
    super
    
    # Modifier keys interceptor
    Modifiers.setup()
    
    # Session
    user = Session.user()

    # Networking
    @atmos = new Atmos(base: 'http://localhost:5000')
    @atmos.bind 'auth_fail', @didFailAuth
    @atmos.bind 'response_error', @didFailResponse
    
    # Routing
    @addRoutesForPages
      '/login'          : 'pages/login_page'
      '/dashboard'      : 'pages/dashboard_page'
      '/categories/new' : 'pages/category_add_page'
      '/error'          : 'pages/error_page'
      '/course/:id'     : 'pages/course_page'
    Spine.Route.setup()
    
    # Default route
    if user
      @navigate '/dashboard'
    else
      @navigate '/login'
  
  addRoutesForPages: (table) ->
    ### Table is in format route -> class path ###
    @pageTable = table
    for routeName, path of table
      Spine.Route.add routeName, @didChangeRoute
    
  didChangeRoute: (match) =>
    input = match.match.input
    matchedRoute = null
    for route in Spine.Route.routes
      matchedRoute = route if route.route.exec(input) 
    
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

window.App = App
module.exports = App
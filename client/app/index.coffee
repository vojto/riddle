require('lib/setup')

Spine = require('spine')
Atmos = require('atmos2')

Session = require('models/session')

LoginPage = require('pages/login_page')
DashboardPage = require('pages/dashboard_page')
CategoryAddPage = require('pages/category_add_page')

class App extends Spine.Controller
  className: 'app'
  
  constructor: ->
    super

    @atmos = new Atmos(base: 'http://localhost:5000')
    
    @addRoutesForPages
      '/login'          : 'pages/login_page'
      '/dashboard'      : 'pages/dashboard_page'
      '/categories/new' : 'pages/category_add_page'
    
    Spine.Route.setup()
    
    user = Session.user()
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
    pagePath = @pageTable[input]
    pageClass = require(pagePath)
    @pageInstances or= {}

    if @pageInstances[pagePath]
      page = @pageInstances[pagePath]
    else
      page = @pageInstances[pagePath] = new pageClass

    if page
      page.show()
      @el.empty()
      @append(page)

module.exports = App
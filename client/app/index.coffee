require('lib/setup')

Spine = require('spine')

LoginPage = require('pages/login_page')
DashboardPage = require('pages/dashboard_page')

class App extends Spine.Controller
  className: 'app'
  
  constructor: ->
    super

    @loginPage = new LoginPage
    @dashboardPage = new DashboardPage
    
    @addRoutesForPages
      '/login': @loginPage
      '/dashboard': @dashboardPage
    
    Spine.Route.setup()
    @navigate '/login'
    
    # TODO: In the future we want to manage stack of pages
  
  addRoutesForPages: (table) ->
    @pageTable = table
    for routeName, page of table
      Spine.Route.add routeName, @didChangeRoute
    
  didChangeRoute: (match) =>
    input = match.match.input
    page = @pageTable[input]
    if page
      page.willShow()
      @el.empty()
      @append(page)

module.exports = App
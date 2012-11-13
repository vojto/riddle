require('lib/setup')

Spine = require('spine')

Session = require('models/session')

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
    
    user = Session.user()
    if user
      @navigate '/dashboard'
    else
      @navigate '/login'
  
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
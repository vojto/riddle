Page = require('lib/page')

LoginView = require('views/login_view')

class LoginPage extends Page
  ### This class represents the login page of teacher interface. ###
  
  constructor: ->
    super

    @loginView = new LoginView
    @append @loginView

module.exports = LoginPage
Page = require('lib/page')

LoginView = require('views/login_view')

class LoginPage extends Page
  ### This class represents the login page of teacher interface. ###
  
  className: 'login-page'
  
  constructor: ->
    super

    @loginView = new LoginView
    @append @loginView

module.exports = LoginPage
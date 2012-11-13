Session = require('models/session')
Page = require('lib/page')

LoginView = require('views/login_view')

class LoginPage extends Page
  ### This class represents the login page of teacher interface. ###
  
  className: 'login-page'
  
  constructor: ->
    super

    @loginView = new LoginView
    @loginView.bind 'login', @didLogin
    @append @loginView
  
  didLogin: (user) ->
    console.log 'logged in', user
    Session.setUser(user)
    @navigate '/dashboard'

module.exports = LoginPage
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
    # TODO: Make request to check if user is logged in
    Session.login user, (res) =>
      if res.response == 'error'
        alert 'Login failed'
      else
        Session.setUser(user)
        @navigate '/dashboard'

module.exports = LoginPage
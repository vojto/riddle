Session = require('models/session')
Page = require('lib/page')

LoginView = require('views/login_view')

class LoginPage extends Page
  ### This class represents the login page of teacher interface. ###
  
  className: 'login-page'
  
  constructor: ->
    super
    
    @addBackgroundLogo()

    @loginView = new LoginView
    @loginView.bind 'login', @didLogin
    @append @loginView
  
  show: ->
    @loginView.reset()
  
  didLogin: (user) =>
    Session.login user, (res) =>
      if res.response == 'error'
        @loginView.showFailed()
      else
        @loginView.hide()
        @logo.addClass('hidden')
        setTimeout =>
          Session.setUser(user)
          @navigate '/dashboard'
        , 500
        

module.exports = LoginPage
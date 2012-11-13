View = require('lib/view')

Session = require('models/session')

class LoginStatusView extends View
  template: require('templates/login_status')
  className: 'login-status'
  
  constructor: ->
    super
    Session.bind 'changeUser', @render
    @render()
  
  render: =>
    @user = Session.user()
    super

module.exports = LoginStatusView
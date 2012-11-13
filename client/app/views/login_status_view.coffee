View = require('lib/view')

Session = require('models/session')

class LoginStatusView extends View
  template: require('templates/login_status')
  
  constructor: ->
    super
    @user = Session.user()
    @render()

module.exports = LoginStatusView
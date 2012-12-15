View = require('lib/view')

Session = require('models/session')

class LoginStatusView extends View
  template: require('templates/login_status')
  className: 'login-status'

  events:
    'click a.log-out': 'logOut'

  constructor: ->
    super
    Session.bind 'changeUser', @render
    @render()

  render: =>
    @user = Session.user()
    super

  logOut: (ev) ->
    ev.preventDefault()
    Session.logout()
    @navigate '/login'

module.exports = LoginStatusView
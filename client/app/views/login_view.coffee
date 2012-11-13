View = require('lib/view')

class LoginView extends View
  ### This class represents interface for entering username and password. ###

  className: 'login'
  template: require('templates/login')

module.exports = LoginView
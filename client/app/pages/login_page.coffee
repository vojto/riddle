Page = require('./page')

class LoginPage extends Page
  ### This class represents the login page of teacher interface. ###
  
  constructor: ->
    super
    console.log 'creating login page'

module.exports = LoginPage
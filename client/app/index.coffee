require('lib/setup')

Spine = require('spine')

LoginPage = require('pages/login_page')

class App extends Spine.Controller
  constructor: ->
    super

    @loginPage = new LoginPage
    @append @loginPage
    # TODO: In the future we want to manage stack of pages

module.exports = App
    
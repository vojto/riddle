Page = require('lib/page')

class ErrorPage extends Page
  constructor: ->
    super
    @append $('<h1 />').addClass('error').text('Internal error. Please try again later.')
    
  show: ->
  
module.exports = ErrorPage
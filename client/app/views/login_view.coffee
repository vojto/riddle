View = require('lib/view')

class LoginView extends View
  ### This class represents interface for entering username and password. ###

  className: 'login'
  template: require('templates/login')
  
  elements:
    'form': '$form'
  
  events:
    'submit form': 'submit'
  
  constructor: ->
    super
  
  submit: (ev) ->
    ev.preventDefault()
    
    data = @$form.serializeObject()
    # TODO: Validate data with the server
    
    @navigate '/dashboard'

module.exports = LoginView
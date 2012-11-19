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
    @$el.bind 'ajaxSend', ->
      $(@).addClass('loading')
    @$el.bind 'ajaxComplete', ->
      $(@).removeClass('loading')
  
  showFailed: ->
    @$el.addClass('failed')
  
  submit: (ev) ->
    ev.preventDefault()
    
    data = @$form.serializeObject()
    @trigger 'login', data

module.exports = LoginView
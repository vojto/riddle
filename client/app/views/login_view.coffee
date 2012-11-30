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
    @render()
    # @$el.bind 'ajaxComplete', ->
      # $(@).removeClass('loading')
  
  showFailed: ->
    @$el.addClass('failed')
  
  reset: ->
    @$el.removeClass('failed')
    @$el.removeClass('loading')
    @$el.removeClass('hidden')
    @$form.find('input[type=text]').val('')
    @$form.find('input[type=password]').val('')
  
  hide: ->
    @$el.addClass('hidden')
  
  submit: (ev) ->
    ev.preventDefault()

    @$el.addClass('loading')
    data = @$form.serializeObject()
    @trigger 'login', data

module.exports = LoginView
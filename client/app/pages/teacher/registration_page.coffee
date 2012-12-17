Atmos = require('atmos2')

Session = require('models/session')
Page = require('lib/page')

RegistrationView = require('views/login_view')

class RegistrationPage extends Page
  className: 'registration-page'
  template: require('templates/registration/form')

  events:
    'submit form': 'submit'

  elements:
    'form': '$form'

  errors:
    already_exists: 'User with the same name already exists'

  constructor: ->
    super

    @addBackgroundLogo()
    @append @template()

  show: ->
    # reset form

  submit: (ev) ->
    ev.preventDefault()

    data = @$form.serializeObject()

    if data.username == '' or data.fullname == '' or data.email == '' or data.password == ''
      App.showError('Please fill in the form')
      return

    @$el.addClass('loading')
    Atmos.res.post '/registration/', data, (res) =>
      @$el.removeClass('loading')
      if res.response == 'success'
        @navigate '/login'
      else
        App.showError(@errors[res.reason])


module.exports = RegistrationPage
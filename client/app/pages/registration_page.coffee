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
    'div.error': '$error'

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
      return

    Atmos.res.post '/registration/', data, (res) =>
      if res.response == 'success'
        @navigate '/login'
      else
        @$error.text(@errors[res.reason] || res.reason)


module.exports = RegistrationPage
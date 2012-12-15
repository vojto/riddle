Atmos = require('atmos2')

Page = require('lib/page')

class LoginPage extends Page
  className: 'light'
  template: require('templates/student/login')

  events:
    'submit form': 'submit'

  elements:
    'form': '$form'

  constructor: ->
    super
    @append @template()

  show: (options) ->
    @courseID = options.course_id

  submit: (ev) ->
    ev.preventDefault()

    data = @$form.serializeObject()
    Atmos.res.post '/student/login/', data, (res) ->
      # TODO: Assert res.success
      Spine.Route.change()

module.exports = LoginPage
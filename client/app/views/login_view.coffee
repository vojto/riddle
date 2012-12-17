View = require('lib/view')

class LoginView extends View
  ### This class represents interface for entering username and password. ###

  className: 'login'
  template: require('templates/login')

  elements:
    'form': '$form'
    '.box': '$box'

  events:
    'submit form': 'submit'
    'click a.registration': 'register'

  constructor: ->
    super
    @render()
    # @$el.bind 'ajaxComplete', ->
      # $(@).removeClass('loading')

  showFailed: ->
    @$el.removeClass('loading')
    @$el.addClass('failed')

    # Shake the box to show failure
    # @$el.find('.box').gfxShake()
    @$el.find('.box').gfx({scale: 1.2}, {duration: 250})
    setTimeout =>
      @$el.find('.box').gfx({scale: 1}, {duration: 250})
    , 300

    App.showError('Login failed')

  reset: ->
    @$el.removeClass('failed')
    @$el.removeClass('loading')
    @$el.removeClass('hidden')
    @$form.find('input[type=text]').val('')
    @$form.find('input[type=password]').val('')
    @$box.gfx({opacity: 1, scale: 1}, {duration: 0})

  hide: ->
    @$box.gfx({opacity: 0, scale: 0.9}, {duration: 500, complete: =>
      @$el.addClass('hidden')
    })

  # Actions

  submit: (ev) ->
    ev.preventDefault()

    @$el.addClass('loading')
    data = @$form.serializeObject()
    @trigger 'login', data

  register: (ev) ->
    ev.preventDefault()
    @navigate '/registration'

module.exports = LoginView
View = require('lib/view')

class CategoryForm extends View
  className: 'category-form'
  template: require('templates/category_form')

  elements:
    'form': '$form'

  events:
    'submit form': 'submit'

  constructor: ->
    super
    @render()
  
  submit: (ev) ->
    ev.preventDefault()
    data = @$form.serializeObject()
    @trigger 'submit', data

module.exports = CategoryForm
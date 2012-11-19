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
    console.log 'creating category', data
    @navigate '/dashboard'

module.exports = CategoryForm
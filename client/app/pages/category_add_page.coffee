Atmos = require('atmos2')
Page = require('lib/page')

CategoryForm = require('views/category_form')

class CategoryAddPage extends Page
  constructor: ->
    super
    
    @addLoginStatus()
    
    @categoryForm = new CategoryForm
    @categoryForm.bind 'submit', @didSubmit
    @append @categoryForm
  
  didSubmit: (data) =>
    Atmos.res.post '/new-category/', data, (res) =>
      @navigate '/dashboard'
  
module.exports = CategoryAddPage
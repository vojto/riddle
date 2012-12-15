Page = require('lib/page')

Category = require('models/category')

CategoryForm = require('views/category_form')

class CategoryAddPage extends Page
  constructor: ->
    super
    
    @addLoginStatus()
    
    @categoryForm = new CategoryForm
    @categoryForm.bind 'submit', @didSubmit
    @append @categoryForm
  
  didSubmit: (data) =>
    Category.createRemote data, =>
      @navigate '/dashboard'
  
module.exports = CategoryAddPage
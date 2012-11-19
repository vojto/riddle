Page = require('lib/page')

CategoryForm = require('views/category_form')

class CategoryAddPage extends Page
  constructor: ->
    super
    
    @addLoginStatus()
    
    @categoryForm = new CategoryForm
    @append @categoryForm
  
module.exports = CategoryAddPage
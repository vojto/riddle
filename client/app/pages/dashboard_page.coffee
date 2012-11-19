Atmos = require('atmos2')

Category  = require('models/category')
Course    = require('models/course')
Page      = require('lib/page')
CategoryListView = require('views/category_list_view')

class DashboardPage extends Page
  className: 'dashboard-page'
  
  constructor: ->
    super
    
    @addLoginStatus()

    @categoryList = new CategoryListView
    @append @categoryList
  
  show: ->
    Category.fetch =>
      @categories = Category.all()
    
      @categoryList.setCategories(@categories)

module.exports = DashboardPage
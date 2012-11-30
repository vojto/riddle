Atmos = require('atmos2')

Page      = require('lib/page')

Category  = require('models/category')
Course    = require('models/course')
CategoryListView = require('views/category_list_view')

class DashboardPage extends Page
  className: 'dashboard-page'
  
  events:
    'click a.add-category': 'addCategory'
  
  constructor: ->
    super
    
    @addLoginStatus()
    
    @append require('templates/dashboard/buttons')() # TODO: Ugly

    @categoryList = new CategoryListView
    @append @categoryList
  
  show: ->
    Category.fetch =>
      Category.trigger('change')
      # @categories = Category.all()
      # @categoryList.setCategories(@categories)
  
  addCategory: ->
    @navigate '/categories/new'

module.exports = DashboardPage
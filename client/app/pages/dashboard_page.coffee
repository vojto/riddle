Page = require('lib/page')

CategoryListView = require('views/category_list_view')

class DashboardPage extends Page
  className: 'dashboard-page'
  
  constructor: ->
    super

    @categoryList = new CategoryListView
    @append @categoryList
  
  willShow: ->
    categories = [
      {name: 'Foo'},
      {name: 'Bar'}
    ]
    
    @categoryList.setCategories(categories)

module.exports = DashboardPage
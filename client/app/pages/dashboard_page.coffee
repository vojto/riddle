Atmos = require('atmos2')

Page      = require('lib/page')

Category  = require('models/category')
Course    = require('models/course')
CategoryListView = require('views/category_list_view')

class DashboardPage extends Page
  className: 'dashboard-page'
  
  events:
    'click a.add-category': 'addCategory'
    'click a.edit': 'edit'
  
  constructor: ->
    super
    
    @isEditing = false
    
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
  
  edit: ->
    @isEditing = !@isEditing
    if @isEditing
      $('a.edit').text('Done')
      @$el.addClass('edit')
    else
      $('a.edit').text('Edit')
      @$el.removeClass('edit')
    

module.exports = DashboardPage
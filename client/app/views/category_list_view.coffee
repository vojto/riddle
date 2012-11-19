View = require('lib/view')
CoursesListView = require('views/courses_list_view')

class CategoryView extends View
  template: require('templates/category')
  
  constructor: (options) ->
    super

    @category = options.model
    @coursesListView = new CoursesListView(courses: @category.courses().all())
    
    @render()
  
  render: ->
    @el.empty()
    @renderTemplate()
    @coursesListView.render()
    @append @coursesListView

class CategoryListView extends View
  @extend Spine.Binding
  
  @binding
    view: CategoryView
    key: 'name'
  
  className: 'ul'

  constructor: (options) ->
    super
  
  setCategories: (categories) ->
    @categories = categories
    @data @categories
    
  
module.exports = CategoryListView
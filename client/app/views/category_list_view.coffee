View = require('lib/view')
CoursesListView = require('views/courses_list_view')

Category = require('models/category')

class CategoryView extends View
  template: require('templates/category')
  
  constructor: (options) ->
    super

    @category = options.model
    @coursesListView = new CoursesListView(courses: @category.courses().all())
    @coursesListView.bind 'createCourse', @createCourse
    @category.bind 'change', =>
      @coursesListView.courses = @category.courses().all()
      @coursesListView.refresh()
    
    @render()
  
  render: ->
    @el.empty()
    @renderTemplate()
    @coursesListView.render()
    @append @coursesListView
  
  createCourse: (data) =>
    @category.createCourseRemote(data)

class CategoryListView extends View
  @extend Spine.Binding
  
  @binding
    view: CategoryView
    key: 'name'
  
  className: 'list'

  constructor: (options) ->
    super
    Category.bind 'change', @refresh
  
  refresh: =>
    @categories = Category.all()
    @data @categories
  
module.exports = CategoryListView
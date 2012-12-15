View = require('lib/view')
CoursesListView = require('views/courses_list_view')

Category = require('models/category')

class CategoryView extends View
  template: require('templates/category')

  elements:
    'h1': '$h1'

  constructor: (options) ->
    super

    @category = options.model
    console.log 'creating new CategoryView for', @category.name

    @renderTemplate()
    @$h1.text(@category.name)

    @coursesListView = new CoursesListView(courses: @category.courses().all())
    @coursesListView.bind 'createCourse', @createCourse
    @append @coursesListView

    @category.bind 'change', =>
      @coursesListView.courses = @category.courses().all()
      @coursesListView.refresh()


  createCourse: (data) =>
    @category.createCourseRemote(data)

class CategoryListView extends View
  @extend Spine.Binding

  @binding
    view: CategoryView
    key: 'id'

  className: 'list'

  constructor: (options) ->
    super
    Category.bind 'change', @refresh

  refresh: =>
    @categories = Category.all()
    @data @categories

module.exports = CategoryListView
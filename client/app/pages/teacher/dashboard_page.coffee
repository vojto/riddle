Atmos = require('atmos2')

Page      = require('lib/page')
View =  require('lib/view')

Category  = require('models/category')
Course    = require('models/course')

## Dashboard
## ----------------------------------------------------------------------------

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
    console.log 'loading dashboard'
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

## Category list
## ----------------------------------------------------------------------------

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

## Courses list
## ----------------------------------------------------------------------------

class AddCourseView extends View
  tag: 'li'
  className: 'add-course'
  template: require('templates/dashboard/add_course')

  elements:
    'span': '$span'
    'input': '$input'

  events:
    'click span': 'activate'
    'keyup input': 'type'

  constructor: ->
    super
    @render()

  activate: ->
    @$el.addClass('active')
    @$input.focus()

  deactivate: ->
    @$el.removeClass('active')

  type: (e) ->
    if e.keyCode == 27
      @deactivate()
    else if e.keyCode == 13
      @deactivate()
      @trigger 'createCourse', {name: @$input.val()}
      @$input.val('')

class CourseView extends View
  tag: 'li'

  events:
    'click': 'didClick'

  constructor: ->
    super
    @render()

  render: ->
    @append @model.name

  didClick: ->
    if App.page.isEditing
      @model.deleteRemote()
    else
      @navigate '/course', @model.public_id

class CoursesListView extends View
  @extend Spine.Binding

  @binding
    view: CourseView
    key: 'id'

  tag: 'ul'
  className: 'course-list'

  constructor: (options) ->
    super
    @courses = options.courses
    @data @courses

    @addCourseView = new AddCourseView()
    @addCourseView.bind 'createCourse', (data) => @trigger 'createCourse', data
    @append @addCourseView

  refresh: ->
    @data @courses
    @append @addCourseView

module.exports = DashboardPage
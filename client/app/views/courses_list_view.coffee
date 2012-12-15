Modifiers = require('lib/modifiers')
View = require('lib/view')

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

module.exports = CoursesListView

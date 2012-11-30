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
  
  constructor: ->
    super
    @render()
  
  render: ->
    @append @model.name

class CoursesListView extends View
  @extend Spine.Binding
  
  @binding
    view: CourseView
    key: 'name'

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
  
  render: ->

module.exports = CoursesListView

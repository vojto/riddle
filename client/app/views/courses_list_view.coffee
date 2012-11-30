View = require('lib/view')

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
  template: require('templates/dashboard/courses_list')
  
  constructor: (options) ->
    super
    @courses = options.courses
    @data @courses
    @append @template()
  
  render: ->

module.exports = CoursesListView

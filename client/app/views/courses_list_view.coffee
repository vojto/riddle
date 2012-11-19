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
  
  constructor: (options) ->
    super
    @courses = options.courses
    @data @courses

module.exports = CoursesListView

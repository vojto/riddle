Page = require('lib/page')
View = require('lib/view')

Course = require('models/course')

class CourseView extends View
  template: require('templates/course/course')

class CoursePage extends Page
  constructor: ->
    super
    @courseView = new CourseView
    @append @courseView
  
  show: (options) ->
    Course.fetchOne options.id, (course) =>      
      @course = course
      @update()
  
  update: ->
    @courseView.course = @course
    @courseView.render()
  
module.exports = CoursePage
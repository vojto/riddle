Page = require('lib/page')
View = require('lib/view')

Course = require('models/course')

# Course page
# -----------------------------------------------------------------------------

class CoursePage extends Page
  constructor: ->
    super
    @courseView = new CourseView
    @append @courseView
    
    @questionListView = new QuestionListView
    @append @questionListView
  
  show: (options) ->
    Course.fetchOne options.id, (course) =>      
      @course = course
      @update()
  
  update: ->
    @courseView.course = @course
    @courseView.render()
    
    @questionListView.course = @course
    @questionListView.update()
  
# Course view
# -----------------------------------------------------------------------------

class CourseView extends View
  template: require('templates/course/course')  

# Question list
# -----------------------------------------------------------------------------

class QuestionView extends View
  template: require('templates/course/question')
  tag: 'li'
  
  constructor: ->
    super
    @render()
  
  render: ->
    super

class QuestionListView extends View
  @extend Spine.Binding
  
  @binding
    view: QuestionView
    key: 'cid'
  
  tag: 'ul'
  
  update: ->
    @questions = @course.questions().all()
    @data @questions


module.exports = CoursePage
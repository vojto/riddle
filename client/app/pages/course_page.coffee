Page = require('lib/page')
View = require('lib/view')

Course = require('models/course')
Question = require('models/question')

# Course page
# -----------------------------------------------------------------------------

class CoursePage extends Page
  constructor: ->
    super
    @courseView = new CourseView
    @append @courseView

    @questionListView = new QuestionListView
    @append @questionListView

    @buttonsView = new ButtonsView
    @buttonsView.bind('addQuestion', @addQuestion)
    @append @buttonsView.render()

  show: (options) ->
    Course.fetchOne options.id, (course) =>
      @course = course
      @update()

  update: ->
    @courseView.course = @course
    @courseView.render()

    @questionListView.course = @course
    @questionListView.update()

  # Actions

  addQuestion: =>
    @navigate '/course', @course.public_id, 'question', 'new'

class ButtonsView extends View
  template: require('templates/course/buttons')

  events:
    'click a.add-question': 'addQuestion'

  addQuestion: ->
    @trigger 'addQuestion'

# Course view
# -----------------------------------------------------------------------------

class CourseView extends View
  template: require('templates/course/course')

# Question list
# -----------------------------------------------------------------------------

class QuestionView extends View
  template: require('templates/course/question')
  tag: 'li'

  events:
    'click a.delete': 'remove'
    'click a.edit-question': 'edit'

  constructor: ->
    super
    @model.bind 'change', @render
    @render()

  render: =>
    super

  # Actions

  remove: (ev) ->
    ev.preventDefault()
    @model.deleteRemote()

  edit: (ev) ->
    ev.preventDefault()
    @navigate '/course', @model.course().public_id, 'question', @model.id


class QuestionListView extends View
  @extend Spine.Binding

  @binding
    view: QuestionView
    key: 'cid'

  tag: 'ul'

  constructor: ->
    super
    Question.bind 'change', @update

  update: =>
    return unless @course
    @questions = @course.questions().all()
    for q, i in @questions
      q.number = i+1
    @data @questions


module.exports = CoursePage
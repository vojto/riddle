Atmos = require('atmos2')
Page = require('lib/page')
View = require('lib/view')

StatusView = require('views/status_view')

Course = require('models/course')
Question = require('models/question')

## Course page
## ----------------------------------------------------------------------------

class CoursePage extends Page
  className: 'has-header light'

  constructor: ->
    super

    @courseView = new CourseView
    @append @courseView

    @questionListView = new QuestionListView
    @append @questionListView

    @buttonsView = new ButtonsView
    @buttonsView.bind('addQuestion', @addQuestion)
    @buttonsView.bind('present', @present)
    @append @buttonsView.render()

    @infoView = new InfoView
    @infoView.hide()
    @append @infoView

    @statusView = new StatusView
    @append @statusView

  show: (options) ->
    @setupHalfling()
    Course.fetchOne options.id, (course) =>
      @course = course
      @update()

  update: ->
    @courseView.course = @course
    @courseView.render()

    @questionListView.course = @course
    @questionListView.update()

    @infoView.course = @course
    @infoView.update()

    @statusView.course = @course
    @statusView.update()

  # Actions

  addQuestion: =>
    @navigate '/course', @course.public_id, 'question', 'new'

  present: =>
    @infoView.show()
    # Start it


class ButtonsView extends View
  template: require('templates/course/buttons')

  events:
    'click a.add-question': 'addQuestion'
    'click a.present': 'present'

  addQuestion: -> @trigger 'addQuestion'
  present: -> @trigger 'present'


## Info view
## ----------------------------------------------------------------------------

class InfoView extends View
  ### This view represents info box with the QR code and URL ###

  template: require('templates/course/info')
  className: 'course-info'
  events:
    'click': 'hide'

  constructor: ->
    super

  update: ->
    host = window.location.host
    @url = "http://#{host}/#/#{@course.public_id}"
    encodedURL = encodeURIComponent(@url)
    @qr = "#{App.base}/qrcode?url=#{encodedURL}"
    @render()

  hide: ->
    @$el.hide()

  show: ->
    @$el.show()


## Course view
## ----------------------------------------------------------------------------

class CourseView extends View
  template: require('templates/course/course')

## Question list
## ----------------------------------------------------------------------------

class QuestionView extends View
  template: require('templates/course/question')
  tag: 'li'
  className: 'clearfix'

  events:
    'click a.delete': 'remove'
    'click a.edit-question': 'edit'
    'click a.present': 'present'

  constructor: ->
    super
    # @model.bind 'change', @render
    @render()

  render: =>
    super

  # Actions

  remove: (ev) ->
    ev.preventDefault()
    @model.deleteRemote()

  edit: (ev) ->
    ev.preventDefault()
    @navigate '/course', @model.course().public_id, 'question', @model.id, 'edit'

  present: (ev) ->
    ev.preventDefault()
    @model.presentRemote()
    @navigate '/course', @model.course().public_id, 'question', @model.id


class QuestionListView extends View
  @extend Spine.Binding

  @binding
    view: QuestionView
    key: 'id'

  tag: 'ul'
  className: 'list question-list'

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
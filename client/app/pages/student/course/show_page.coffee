Atmos = require('atmos2')

Page = require('lib/page')
View = require('lib/view')

Course = require('models/course')
Question = require('models/question')

## Show page

class ShowPage extends Page
  template: require('templates/student/course/show')
  className: 'light'

  ## Lifecycle

  constructor: ->
    super
    @question = null
    @questionView = new QuestionView

  show: (options) ->
    @courseID = options.course_id
    Atmos.res.get '/student/status', (res) =>
      if !res
        @navigate '/student/login', course_id: @courseID, shim: true
      else
        @studentID = res.id
        @showAfterAuth()

  showAfterAuth: ->
    # Fetch the course
    Course.studentMode = true
    Course.fetchOne @courseID, (course) =>
      @course = course
      @render()

      @refreshRemote()

  render: ->
    super
    return unless @course
    @html @template(@)
    @append @questionView

  update: ->
    @questionView.question = @question
    @questionView.update()

  ## Pinging

  refreshRemote: =>
    console.log 'pinging...'
    Atmos.res.get "/student/ping/#{@course.public_id}/", (res) =>
      if res.presented_question
        question = Question.find(res.presented_question)
        if !@question or (@question.id != question.id)
          @question = question
          @update()

      setTimeout(@refreshRemote, 2000)

## Question view

class QuestionView extends View
  template: require('templates/student/course/question')

  events:
    'submit form': 'submit'

  elements:
    'form': '$form'

  update: ->
    if @question
      @options = @question.options().all()
    @render()

  ## Actions

  submit: (ev) ->
    ev.preventDefault()
    console.log 'submitting'

    data = @$form.serializeObject()
    data.question_id = @question.id

    console.log 'submitting answer', data
    Atmos.res.post "/submit-answer/", data, (res) =>
      @question.isSubmitted = true
      @question.save()
      console.log 'submitted answer', res
      @update()


module.exports = ShowPage
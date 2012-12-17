Atmos = require('atmos2')

Page = require('lib/page')
View = require('lib/view')

Course = require('models/course')
Question = require('models/question')

## Show page

class ShowPage extends Page
  template: require('templates/student/course/show')
  className: 'light student-question'

  elements:
    'div.content': '$content'

  ## Lifecycle

  constructor: ->
    super
    @question = null
    @questionView = new QuestionView
    @commentView = new CommentFormView

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
      console.log course
      @render()

      @refreshRemote()

  render: ->
    super
    return unless @course
    @html @template(@)
    @$content.append(@questionView.el)
    @$content.append(@commentView.el)

  update: ->
    @questionView.question = @question
    @questionView.update()
    @commentView.question = @question
    @commentView.update()

  ## Pinging

  refreshRemote: =>
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
    'tap li.option': 'selectOption'

  elements:
    'form': '$form'
    'ul': '$ul'

  update: ->
    if @question
      @options = @question.options().all()
    @render()


  ## Event handlers

  selectOption: (ev) ->
    @$ul.find('li').removeClass('active')
    $option = $(ev.currentTarget)
    id = $option.attr('data-id')
    $option.addClass('active')
    console.log 'selecting option lol'

    data = {
      'option_ids[]': id,
      question_id: @question.id
    }

    Atmos.res.post "/submit-answer/", data, (res) =>
      @question.isSubmitted = true
      @question.save()
      console.log 'submitted answer', res
      @update()


## Comment form view

class CommentFormView extends View
  template: require('templates/student/course/comment_form')

  events:
    'submit form': 'submit'

  elements:
    'form': '$form'

  constructor: ->
    super
    @update()

  submit: (ev) ->
    ev.preventDefault()
    {comment} = @$form.serializeObject()
    return if comment == ''

    data = {
      question_id: @question.id,
      text_answer: comment
    }

    Atmos.res.post '/submit-answer/', data, (res) ->
      console.log 'submitted answer', res

    @isSubmitted = true
    @render()

  update: ->
    @isSubmitted = false
    @render()

module.exports = ShowPage
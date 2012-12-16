Atmos = require('atmos2')
Page = require('lib/page')

Course = require('models/course')

class QuestionPage extends Page
  ###
  Page for displaying question real-time stats
  ###

  template: require('templates/question/show')

  constructor: ->
    super
    @question = null

  show: (options) ->
    courseID = options.course_id
    questionID = options.id

    Course.fetchOne courseID, (course) =>
      @course = course
      @question = @course.questions().find(questionID)
      options = @question.options()

      @update()

      # Get the results
      Atmos.res.post '/results-options/', {question_id: @question.id}, (res) =>
        answers = res.question_answers
        for optionData in answers
          option = options.find(optionData.option_id)
          option.answerCount = optionData.answers
          option.save()
        @update()

  render: ->
    super
    if @course and @question
      @options = @question.options().all()
      @html @template(@)

  update: ->
    @render()

module.exports = QuestionPage
Page = require('lib/page')

Course = require('models/course')
Question = require('models/question')

class QuestionFormPage extends Page
  template: require('templates/question/form')

  elements:
    'form': '$form'

  events:
    'submit form': 'submit'

  constructor: ->
    super
    @html @template()

  show: (options) ->
    Course.fetchOne options.course_id, (course) =>
      @course = course

  # Actions

  submit: (ev) ->
    ev.preventDefault()

    # 01 Get data
    data = @$form.serializeObject()
    # return unless data.description # TODO: Could use real validation

    # 02 Create the object
    data.course = @course
    question = new Question(data)
    question.createRemote =>
      console.log 'created question'
      @navigate '/course', @course.public_id

module.exports = QuestionFormPage
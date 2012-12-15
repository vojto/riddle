Atmos = require('atmos2')
Spine = require('spine')

Question = require('models/question')

class Course extends Spine.Model
  @configure 'Course', 'name', 'public_id'
  @belongsTo 'category', 'models/category'
  @hasMany 'questions', 'models/question'

  deleteRemote: ->
    Atmos.res.post '/remove-questionnaire/', {id: @id}, (res) =>
      @destroy()
      @category().trigger 'change'

  @fetchOne: (id, callback) ->
    Atmos.res.get "/qaires/#{id}", (res) ->
      questions = res.questions
      delete res.questions
      course = new Course(res)
      course.save()

      for questionData in questions
        questionData.course = course
        question = new Question(questionData)
        question.save()

      callback(course)


module.exports = Course
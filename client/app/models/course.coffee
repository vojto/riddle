Atmos = require('atmos2')
Spine = require('spine')

class Course extends Spine.Model
  @configure 'Course', 'name', 'public_id'
  @belongsTo 'category', 'models/category'
  
  deleteRemote: ->
    Atmos.res.post '/remove-questionnaire/', {id: @id}, (res) =>
      @destroy()
      @category().trigger 'change'
  
  @fetchOne: (id, callback) ->
    Atmos.res.get "/qaires/#{id}", (res) ->
      questions = res.questions
      delete res.questions
      course = new Course(res)
      
      # TODO: For each question, create question object
      # and associate it with course object.
      
      callback(course)
      
  
module.exports = Course
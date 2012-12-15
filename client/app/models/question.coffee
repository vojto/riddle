Spine = require('spine')
Atmos = require('atmos2')

class Question extends Spine.Model
  @configure 'Question', 'presented', 'type', 'description'
  @belongsTo 'course', 'models/course'
  @hasMany 'options', 'models/option'

  createRemote: (callback) ->
    optionsData = @options().all().map (o) -> o.text
    data = {
      type: @type,
      description: @description,
      public_id: @course().public_id
      options: optionsData
    }
    Atmos.res.post '/new-question/', data, (res) =>
      # TODO: Handle error
      @id = res.question_id
      callback(@)


module.exports = Question
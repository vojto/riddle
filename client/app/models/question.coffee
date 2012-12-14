Spine = require('spine')
Atmos = require('atmos2')

class Question extends Spine.Model
  @configure 'Question', 'presented', 'type', 'description'
  @belongsTo 'course', 'models/course'

  createRemote: (callback) ->
    data = {
      type: @type,
      description: @description,
      public_id: @course().public_id
    }
    console.log 'creating question with data: ', data
    Atmos.res.post '/new-question/', data, (res) ->
      console.log 'finished', res


module.exports = Question
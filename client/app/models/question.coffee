Spine = require('spine')
Atmos = require('atmos2')

Option = require('models/option')

class Question extends Spine.Model
  @configure 'Question', 'presented', 'type', 'description'
  @belongsTo 'course', 'models/course'
  @hasMany 'options', 'models/option'
  @hasMany 'comments', 'models/comment'

  updateOrCreateRemote: (callback) ->
    optionsData = @options().all().map (o) -> o.text
    data = {
      type: @type,
      description: @description,
      public_id: @course().public_id
      options: optionsData
    }

    if @isNew()
      path = '/new-question/'
    else
      path = '/edit-question/'
      data.id = @id

    Atmos.res.post path, data, (res) =>
      # TODO: Handle error
      @id = res.question_id
      @save()
      # @changeID(res.question_id)
      callback(@)

  deleteRemote: ->
    Atmos.res.post '/remove-question/', {id: @id}, (res) =>
      console.log 'deleted question lol', res
    @destroy()

  presentRemote: ->
    Atmos.res.get "/present-question/#{@id}/", (res) ->
      console.log 'presneted question', res

  load: (data) ->
    super
    if data.options
      for optionData in data.options
        optionData.question = @
        option = new Option(optionData)
        option.save()

module.exports = Question
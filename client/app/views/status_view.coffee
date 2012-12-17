Atmos = require('atmos2')
View = require('lib/view')

Question = require('models/question')

class StatusView extends View
  ### Presentation status view ###

  template: require('templates/course/status')
  className: 'presentation-status'

  constructor: ->
    super
    @connectedUsers = 0
    @currentQuestion = null
    @render()

  update: ->
    @refreshRemote()

  refreshRemote: =>
    return unless @course
    Atmos.res.get "/status/#{@course.public_id}", (res) =>
      @connectedUsers = res.student_count
      if res.presented_question
        @currentQuestion = new Question(res.presented_question)

      @render()
      setTimeout @refreshRemote, 2000

module.exports = StatusView
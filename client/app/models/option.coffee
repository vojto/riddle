Spine = require('spine')

class Option extends Spine.Model
  @configure 'Option', 'text', 'answerCount'
  @belongsTo 'question', 'models/question'

  load: ->
    super
    @answerCount or= 0

module.exports = Option
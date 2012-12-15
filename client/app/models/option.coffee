Spine = require('spine')

class Option extends Spine.Model
  @configure 'Option', 'text'
  @belongsTo 'question', 'models/question'

module.exports = Option
Spine = require('spine')

class Question extends Spine.Model
  @configure 'Question', 'presented', 'type', 'description'
  @belongsTo 'course', 'models/course'

module.exports = Question
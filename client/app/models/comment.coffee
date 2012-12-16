Spine = require('spine')

class Comment extends Spine.Model
  @configure 'Comment', 'student', 'text'
  @belongsTo 'question', 'models/question'

module.exports = Comment
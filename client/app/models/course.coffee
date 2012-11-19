Spine = require('spine')

class Course extends Spine.Model
  @configure 'Course', 'name'
  @belongsTo 'category', 'models/category'

module.exports = Course
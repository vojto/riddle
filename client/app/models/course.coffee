Atmos = require('atmos2')
Spine = require('spine')

class Course extends Spine.Model
  @configure 'Course', 'name', 'public_id'
  @belongsTo 'category', 'models/category'
  
  deleteRemote: ->
    Atmos.res.post '/remove-questionnaire/', {id: @id}, (res) =>
      @destroy()
      @category().trigger 'change'
  
module.exports = Course
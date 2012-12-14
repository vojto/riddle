Page = require('lib/page')

class CoursePage extends Page
  constructor: ->
    super
    @append 'this is the lecture page'
  
module.exports = CoursePage
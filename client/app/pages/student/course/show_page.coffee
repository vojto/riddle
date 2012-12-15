Atmos = require('atmos2')

Page = require('lib/page')

Course = require('models/course')

class ShowPage extends Page
  template: require('templates/student/course/show')
  className: 'light'

  constructor: ->
    super

  show: (options) ->
    @courseID = options.course_id
    Atmos.res.get '/student/status', (res) =>
      if !res
        @navigate '/student/login', course_id: @courseID, shim: true
      else
        @loadCourse()

  loadCourse: ->
    Course.fetchOne @courseID, (course) =>
      @course = course
      @render()

  render: ->
    super
    return unless @course
    console.log 'rendering', @course
    @html @template(@)


module.exports = ShowPage
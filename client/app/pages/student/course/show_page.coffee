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
        @studentID = res.id
        @showAfterAuth()

  showAfterAuth: ->
    # Fetch the course
    Course.fetchOne @courseID, (course) =>
      @course = course
      @render()

      @notifier = new StudentPresenceNotifier(studentID: @studentID, courseID: @courseID)

  render: ->
    super
    return unless @course
    console.log 'rendering', @course
    @html @template(@)

## Student presence notifier

class StudentPresenceNotifier extends Spine.Module
  constructor: (options) ->
    @courseID = options.courseID
    @studentID = options.studentID

    @notify()

  notify: =>
    console.log 'pinging...'
    Atmos.res.get "/student/ping/#{@courseID}/", (res) =>
      console.log 'completed ping', res
      setTimeout(@notify, 2000)


module.exports = ShowPage
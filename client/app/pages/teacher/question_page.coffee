Atmos = require('atmos2')
Page = require('lib/page')
View = require('lib/view')

StatusView = require('views/status_view')

Course = require('models/course')
Comment = require('models/comment')

class QuestionPage extends Page
  ###
  Page for displaying question real-time stats
  ###

  template: require('templates/question/show')
  className: 'has-header light'

  elements:
    'svg#graph': '$graph'
    'h1': '$h1'

  constructor: ->
    super
    @html @template(@)
    @question = null

    @commentsView = new CommentsView
    @append @commentsView

    @statusView = new StatusView
    @append @statusView

  show: (options) ->
    @setupHalfling()

    courseID = options.course_id
    questionID = options.id

    Course.fetchOne courseID, (course) =>
      @course = course
      @question = @course.questions().find(questionID)

      @update()

      # Get the results
      @fetchResults()

  fetchResults: =>
    data = {question_id: @question.id}

    Atmos.res.post '/results-options/', data, (res) =>
      options = @question.options()
      answers = res.question_answers
      return unless answers
      for optionData in answers
        option = options.find(optionData.option_id)
        option.answerCount = optionData.answers
        option.save()
      @update()

    Atmos.res.post '/results-texts/', data, (res) =>
      for commentData in res.question_answers
        commentData.question = @question
        try
          comment = @question.comments().exists(commentData.id)
        catch e
          comment = new Comment(commentData)
        comment.save()
      @commentsView.comments = @question.comments().all()
      @commentsView.update()

    setTimeout @fetchResults, 2000

  renderGraph: =>
    console.log 'rendering graph'

    options = @question.options().all()
    data = options.map (o) -> {label: o.text, value: o.answerCount}
    maxValue = d3.max(data, (d) -> d.value)
    maxValue = 1 if maxValue == 0 # division by zero

    totalWidth = 400
    totalHeight = 100
    padding = 5
    width = (totalWidth / data.length) - padding

    # Scales
    y = (d, i) -> (d.value/maxValue)*totalHeight
    x = (d, i) -> i * (width + padding)
    color = d3.scale.category20c()

    @graph3 = d3.select(@$graph.get(0))
    @graph3.attr('width', totalWidth).attr('height', totalHeight + 20)

    bars = @graph3.selectAll('rect').data(data)
    bars.enter().append('rect')
      .attr('width', width)
      .attr('y', totalHeight)
      .attr('x', x)
      .attr('fill', (d, i) -> color(i))
    bars.transition()
      .attr('x', x)
      .attr('y', (d, i) -> totalHeight-y(d, i))
      .attr('width', width)
      .attr('height', y)

    values = @graph3.selectAll('text.value').data(data)
    values.enter().append('text')
      .attr('class', 'value')
      .attr('fill', '#fff')
      .attr('y', totalHeight+20)
    values.transition().attr('x', (d, i) -> x(d, i) + 10)
      .attr('y', (d) -> totalHeight-y(d)+20)
      .text((d) -> d.value)

    labels = @graph3.selectAll('text.label').data(data)
    labels.enter().append('text')
      .attr('class', 'label')
      .attr('fill', '#000')
      .style('font-weight', 'bold')
    labels.attr('x', (d, i) -> x(d, i) + 10)
      .attr('y', (d) -> totalHeight + 20)
      .text((d) -> d.label)


  update: ->
    @statusView.course = @course
    @statusView.update()

    if @question
      @$h1.text(@question.description)
      if @question.type == 3
        @$graph.hide()
      else
        @$graph.show()
        @renderGraph()

## Comments view

class CommentView extends View
  template: require('templates/question/comment')

  constructor: ->
    super
    @render()

class CommentsView extends View
  @extend Spine.Binding

  @binding
    view: CommentView
    key: 'id'

  className: 'comments'

  constructor: ->
    super

  update: ->
    @data @comments

module.exports = QuestionPage
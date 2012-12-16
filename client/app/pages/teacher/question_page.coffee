Atmos = require('atmos2')
Page = require('lib/page')

Course = require('models/course')

class QuestionPage extends Page
  ###
  Page for displaying question real-time stats
  ###

  template: require('templates/question/show')
  className: 'light'

  elements:
    'svg#graph': '$graph'

  constructor: ->
    super
    @question = null

  show: (options) ->
    courseID = options.course_id
    questionID = options.id

    Course.fetchOne courseID, (course) =>
      @course = course
      @question = @course.questions().find(questionID)
      options = @question.options()

      @update()

      # Get the results
      Atmos.res.post '/results-options/', {question_id: @question.id}, (res) =>
        answers = res.question_answers
        for optionData in answers
          option = options.find(optionData.option_id)
          option.answerCount = optionData.answers
          option.save()
        @update()

  render: ->
    super
    if @course and @question
      # Render the template
      @options = @question.options().all()
      @html @template(@)

      # Render the graph!
      @renderGraph()

  renderGraph: ->
    data = [{label: 'foo', value: 5}, {label: 'bar', value: 10}]
    maxValue = d3.max(data, (d) -> d.value)

    totalWidth = 400
    totalHeight = 200
    padding = 5
    width = (totalWidth / data.length) - padding

    # Scales
    y = (d, i) -> (d.value/maxValue)*totalHeight
    x = (d, i) -> i * (width + padding)
    color = d3.scale.category20c()

    graph3 = d3.select(@$graph.get(0))
    graph3.attr('width', totalWidth).attr('height', totalHeight + 20)
    enter = graph3.selectAll('rect')
      .data(data)
      .enter()
    enter.append('rect')
      .attr('x', x)
      .attr('y', (d) -> totalHeight-y(d))
      .attr('width', width)
      .attr('height', y)
      .attr('fill', (d, i) -> color(i))
    enter.append('text')
      .attr('x', (d, i) -> x(d, i) + 10)
      .attr('y', (d) -> totalHeight-y(d)+20)
      .text((d) -> d.value)
      .attr('fill', '#fff')
    enter.append('text')
      .attr('x', (d, i) -> x(d, i) + 10)
      .attr('y', (d) -> totalHeight + 20)
      .text((d) -> d.label)
      .attr('fill', '#000')
      .style('font-weight', 'bold')

  update: ->
    @render()

module.exports = QuestionPage
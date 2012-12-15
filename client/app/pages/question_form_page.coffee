Page = require('lib/page')
View = require('lib/view')

Course = require('models/course')
Question = require('models/question')
Option = require('models/option')

# QuestionFormPage
# -----------------------------------------------------------------------------
class QuestionFormPage extends Page
  template: require('templates/question/form')

  elements:
    'form': '$form'

  events:
    'submit form': 'submit'
    'click a.add-option': 'addOption'

  constructor: ->
    super

    @html @template()

    @optionListView = new OptionListView
    @$('div.options').append(@optionListView.$el)

  show: (options) ->
    Course.fetchOne options.course_id, (course) =>
      @course = course

  # Actions

  submit: (ev) ->
    ev.preventDefault()

    # 01 Get data
    data = @$form.serializeObject()
    # return unless data.description # TODO: Could use real validation

    # 02 Create the object
    @question = new Question
    @question.course_id = @course.id
    @question.load(data)
    @question.save()

    # 03 Get options
    options = for option in @optionListView.nonEmptyOptions()
      option.question_id = @question.id
      option.save()
      option

    console.log 'creating question', @question
    @question.createRemote =>
      console.log 'created question'
      @navigate '/course', @course.public_id

  addOption: (ev) ->
    ev.preventDefault()
    @optionListView.createOption()

# OptionView
# -----------------------------------------------------------------------------
class OptionView extends View
  template: require('templates/question/option')

  events:
    'keyup input': 'updateModel'

  constructor: ->
    super
    @render()

  updateModel: ->
    @model.text = @$('input').val()

# OptionListView
# -----------------------------------------------------------------------------
class OptionListView extends View
  @extend Spine.Binding

  @binding
    view: OptionView
    key: 'cid'

  constructor: ->
    super
    @options = []

    @append 'this is option list view'
    @update()

  update: ->
    console.log 'updating them options', @options
    @data @options

  # Actions

  createOption: ->
    opt = new Option
    opt.save()
    @options.push(opt)
    @update()

  # Accessors

  nonEmptyOptions: ->
    @options.filter (o) ->
      o.text && (o.text != '')

module.exports = QuestionFormPage
Page = require('lib/page')
View = require('lib/view')

Course = require('models/course')
Question = require('models/question')
Option = require('models/option')

# QuestionFormPage
# -----------------------------------------------------------------------------
class QuestionFormPage extends Page
  template: require('templates/question/form')
  className: 'light halfling'

  elements:
    'form': '$form'
    'input[name=description]': '$descriptionField'
    'select[name=type]': '$typeSelect'

  events:
    'submit form': 'submit'
    'click a.add-option': 'addOption'

  constructor: ->
    super

    @html @template()

    @optionListView = new OptionListView
    @$('div.options').append(@optionListView.$el)

  show: (options) ->
    courseID = options.course_id
    questionID = options.id

    @isEditing = !!questionID
    Course.fetchOne courseID, (course) =>
      @course = course
      if @isEditing
        @question = @course.questions().find(questionID)
        @question.bind 'change', @update
      @update()

  update: =>
    ### Updates the form and options list ###
    if @question
      @$descriptionField.val(@question.description)
      @$typeSelect.val(@question.type)
      @optionListView.options = @question.options().all()
    @optionListView.update()


  # Actions

  submit: (ev) ->
    ev.preventDefault()

    # 01 Get data
    data = @$form.serializeObject()
    # return unless data.description # TODO: Could use real validation

    # 02 Create the object if needed
    @question or= new Question
    @question.course_id = @course.id
    @question.load(data)

    # 03 Get options
    options = for option in @optionListView.nonEmptyOptions()
      option.question_id = @question.id
      option.save()
      option

    console.log 'creating question', @question
    @question.updateOrCreateRemote =>
      console.log 'created question'
      @navigate '/course', @course.public_id

  addOption: (ev) ->
    ev.preventDefault()
    @optionListView.createOption()

# OptionView
# -----------------------------------------------------------------------------
class OptionView extends View
  template: require('templates/question/option')

  elements:
    'input': '$input'

  events:
    'keyup input': 'updateModel'

  constructor: ->
    super
    @render()
    @$input.val(@model.text)

  updateModel: ->
    @model.text = @$input.val()

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
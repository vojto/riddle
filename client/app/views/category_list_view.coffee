View = require('lib/view')

class CategoryView extends View
  template: require('templates/category')
  
  constructor: (options) ->
    @category = options.model
    super
  
  render: ->
    super

class CategoryListView extends View
  @extend Spine.Binding
  
  @binding
    view: CategoryView
    key: 'name'
  
  className: 'ul'

  constructor: (options) ->
    super
  
  setCategories: (categories) ->
    @categories = categories
    @data @categories
    
  
module.exports = CategoryListView
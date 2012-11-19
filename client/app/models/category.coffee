Atmos = require('atmos2')
Spine = require('spine')

Course = require('models/course')

class Category extends Spine.Model
  @configure 'Category', 'name'
  @hasMany 'courses', 'models/course'
  
  @fetch: (callback) ->
    # Do a little custom request here, because the response returned from
    # server is not in the form of simple collection, so we can't use Atmos2
    # fetching/caching facilities.

    Atmos.res.get '/qaires/', (res) ->
      for category in res
        categoryModel = new Category({name: category.category})
        categoryModel.save()

        for course in category.questionnaires
          courseModel = new Course({name: course.name, category: categoryModel})
          courseModel.save()
      
      callback()

module.exports = Category
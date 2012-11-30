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

    Atmos.res.get '/qaires/', (res) =>
      for category in res
        categoryModel = new Category({name: category.category, id: category.id})
        categoryModel.save()

        for course in category.questionnaires
          courseModel = new Course({name: course.name, public_id: course.public_id, category: categoryModel})
          courseModel.save()
        
        categoryModel.trigger('change') # Because we added course
      
      callback()
  
  @createRemote: (data, callback) ->
    Atmos.res.post '/new-category/', data, (res) ->
      callback()
  
  createCourseRemote: (data) ->
    data.category_id = @id
    Atmos.res.post '/new-questionnaire/', data, (res) =>
      course = new Course({name: data.name, category: @, public_id: res.public_id})
      course.save()
      @trigger('change')

module.exports = Category
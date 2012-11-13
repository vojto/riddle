Spine = require('spine')

class Persistence extends Spine.Module
  @set: (key, value) ->
    localStorage["riddle.#{key}"] = JSON.stringify(value)
  
  @get: (key) ->
    value = localStorage["riddle.#{key}"]
    if value then JSON.parse(value) else null

class Session extends Spine.Module
  @extend Spine.Events
  
  @setUser: (user) ->
    Persistence.set 'currentUser', user
    @trigger 'changeUser'
  
  @user: ->
    Persistence.get 'currentUser'
  
module.exports = Session
Spine = require('spine')

class Persistence extends Spine.Module
  @set: (key, value) ->
    localStorage["riddle.#{key}"] = JSON.stringify(value)
  
  @get: (key) ->
    JSON.parse(localStorage["riddle.#{key}"])

class Session extends Spine.Module
  @setUser: (user) ->
    Persistence.set 'currentUser', user
  
  @user: ->
    Persistence.get 'currentUser'
  
module.exports = Session
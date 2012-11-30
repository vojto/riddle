class Modifiers
  @setup: ->
    $(document).bind 'keydown', @keydown
    $(document).bind 'keyup', @keyup
  
  @keydown: (e) =>
    @alt = e.altKey
    @update()
  
  @keyup: (e) =>
    @alt = e.altKey
    @update()
  
  @update: ->
    if @alt
      $(document.body).addClass('alt')
    else
      $(document.body).removeClass('alt')

module.exports = Modifiers
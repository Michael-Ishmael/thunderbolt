Spine = require('spine')

class Navigation extends Spine.Model
  @configure 'Navigation', 'heading', 'area'

  constructor: ->
    super

  @load: ->
    source = Navigation.create({heading: "Sources", area: "source"})
    source = Navigation.create({heading: "Documents", area: "document"})

module.exports = Navigation

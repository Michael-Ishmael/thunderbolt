require('lib/setup')

Spine = require('spine')
Docheaders = require('controllers/docheaders')

class App extends Spine.Controller
  constructor: ->
    super
    @docheaders = new Docheaders
    @append @docheaders

    Spine.Route.setup()

module.exports = App
    
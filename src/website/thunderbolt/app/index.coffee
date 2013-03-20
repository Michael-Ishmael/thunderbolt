require('lib/setup')

Spine = require('spine')
Docheaders = require('controllers/docheaders')

class App extends Spine.Controller
  className: 'prodApp'

  constructor: ->
    super
    @docheaders = new Docheaders({el: $("#docs")})
    @append @docheaders

    Spine.Route.setup()

module.exports = App

#open -a Google\ Chrome --args --disable-web-security
    
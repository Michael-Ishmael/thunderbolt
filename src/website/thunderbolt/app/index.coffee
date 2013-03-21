require('lib/setup')

Spine = require('spine')
Navigator = require('controllers/navigator')
Navigation = require('models/navigation')
DocHeader = require('controllers/docheaders_list')

class App extends Spine.Controller
  className: 'prodApp'

  constructor: ->
    super
    @navigator = new Navigator({el: $("#navigation")})
    @append @navigator

    Spine.Route.setup()

    Navigation.load()

    #Navigation.fetch()


module.exports = App

#open -a Google\ Chrome --args --disable-web-security
    
require('lib/setup')

Spine = require('spine')
Navigator = require('controllers/navigator')
Navigation = require('models/navigation')
Document = require('models/docheader')
Source = require('models/source')
Main = require('controllers/main')

class App extends Spine.Controller
  className: 'prodApp'

  constructor: ->
    super
    @navigator = new Navigator(el: $("#navigation"))
    @main = new Main(el: $('#main'))


    Spine.Route.setup()

    Document.fetch()
    Source.fetch()

    Navigation.load()

    @navigator.change(Navigation.first())


module.exports = App

#open -a Google\ Chrome --args --disable-web-security
    
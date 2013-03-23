Spine = require('spine')
Navigation = require('models/navigation')
List = require('spine/lib/list')
$ = Spine.$

class Navigator extends Spine.Controller
  className: 'navigator'

  elements:
    'ul.navigation': 'navBar'

  events:
    'click ul.navigation li': 'navigate'

  constructor: ->
    super

    @list = new List
      el: @navBar,
      template: (items) ->
        lstHtml = ''
        for item in items
          lstHtml += '<li class="item">'+item.heading+'</li>'
        return lstHtml
      selectFirst: false

    @list.bind 'change', @change

    @active (params) ->
      @list.change(Navigation.find(params.id))

    Navigation.bind('refresh change', @render)

  render: =>
    navs = Navigation.all()
    @list.render(navs)

  change: (item) =>
    @navigate '/' + item.area

    
module.exports = Navigator
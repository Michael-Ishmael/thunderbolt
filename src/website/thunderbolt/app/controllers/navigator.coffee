Spine = require('spine')
Navigation = require('models/navigation')
List = require('spine/lib/list')
$ = Spine.$

class Navigator extends Spine.Controller
  className: 'navigator'

  elements:
    'ul.navigation': 'items'

  events:
    'click ul.navigation li': 'navigate'

  constructor: ->
    super
    @html require('views/navigation')()

    @list = new List
      el: @items,
      template: (items) ->
        lstHtml = ''
        for item in items
          lstHtml += '<li>'+item.heading+'</li>'
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
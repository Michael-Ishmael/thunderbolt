Spine = require('spine')
Source = require('models/source')
List = require('spine/lib/list')
$ = Spine.$

class Sources extends Spine.Controller
  className: 'sources'
  tag: 'table'

  elements:
    '.items': 'items'
    'input[type=search]': 'search'

  events:
    'keyup input[type=search]': 'filter'
    'click footer button': 'create'

  constructor: ->
    super
    @html require('views/sources')(@item)

    @list = new List
      el: @items,
      template: require('views/source'),
      selectFirst: false

    @list.bind 'change', @change

    @active (params) ->
      if params.id
        @list.change(Source.find(params.id))

    Source.bind('refresh change', @render)

  filter: ->
    @query = @search.val()
    @render()

  render: =>
    docs = Source.filter(@query)
    @list.render(docs)

  change: (item) =>
    @navigate '/sourceEdit', item.id

  create: ->
    item = Source.create()
    @navigate '/sources', item.id, 'edit'




module.exports = Sources
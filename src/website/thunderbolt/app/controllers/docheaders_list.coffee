Spine = require('spine')
Docheader = require('models/docheader')
List = require('spine/lib/list')
$ = Spine.$

class DocHeaderList extends Spine.Controller
  className: 'docList'

  elements:
    '.items': 'items'
    'input[type=search]': 'search'

  events:
    'keyup input[type=search]': 'filter'
    'click footer button': 'create'

  constructor: ->
    super
    @html require('views/documentlist')(@item)

    @list = new List
      el: @items,
      template: require('views/docheader'),
      selectFirst: false

    @list.bind 'change', @change

    @active (params) ->
      @list.change(Docheader.find(params.id))

    Docheader.bind('refresh change', @render)

  filter: ->
    @query = @search.val()
    @render()

  render: =>
    docs = Docheader.filter(@query)
    @list.render(docs)

  change: (item) =>
    @navigate '/documents', item.id

  create: ->
    item = Docheader.create()
    @navigate '/documents', item.id, 'edit'

    
module.exports = DocHeaderList
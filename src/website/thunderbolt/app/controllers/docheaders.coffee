Spine = require('spine')
Docheader = require('models/docheader')
$ = Spine.$

DocList = require('controllers/docheaders_list')

class Docheaders extends Spine.Controller
  constructor: ->
    super

    @docList = new DocList

    @routes
      '/documents/:id/edit': (params) ->
        @docList.active(params)
      '/documents/:id': (params) ->
        @docList.active(params)

    @append @docList

    Docheader.fetch()
    
module.exports = Docheaders
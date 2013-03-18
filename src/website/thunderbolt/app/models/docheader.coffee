Spine = require('spine')

class Docheader extends Spine.Model
  @configure 'Docheader', 'id', 'title', 'date', 'sourceId' #, 'url', 'sourceName', 'sourceId', 'analystName', 'analystId', 'status', 'rel'

  @extend Spine.Model.Ajax

  @url: "http://localhost:8081/document"

  @filter: (query) ->
    return @all() unless query
    query = query.toLowerCase()
    @select (item) ->
      item.title?.toLowerCase().indexOf(query) isnt -1

module.exports = Docheader
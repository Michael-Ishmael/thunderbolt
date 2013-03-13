Spine = require('spine')

class Docheader extends Spine.Model
  @configure 'Docheader', 'id', 'title', 'date', 'url', 'sourceName', 'sourceId', 'analystName', 'analystId', 'status', 'rel'

  @extend @Local

  @filter: (query) ->
    return @all() unless query
    query = query.toLowerCase()
    @select (item) ->
      item.title?.toLowerCase().indexOf(query) isnt -1

module.exports = Docheader
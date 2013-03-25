Spine = require('spine')

class Source extends Spine.Model
  @configure 'Source', 'id', 'title', 'readership', 'pageRate'

  @extend Spine.Model.Ajax

  @url: "http://localhost:8081/source"

  @filter: (query) ->
    return @all() unless query
    query = query.toLowerCase()
    @select (item) ->
      item.title?.toLowerCase().indexOf(query) isnt -1

  @load: () ->
    one = Source.create({title: "Source 1", readership: 208902})
    two = Source.create({title: "Source 2", readership: 2780003})

module.exports = Source
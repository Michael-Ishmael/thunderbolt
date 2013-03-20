Spine = require('spine')

class Source extends Spine.Model
  @configure 'Source', 'id', 'title', 'readership', 'pageRate'

  @url: "http://localhost:8081/source"
  
module.exports = Source
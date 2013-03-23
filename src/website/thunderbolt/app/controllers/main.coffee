Spine = require('spine')
Documents = require('controllers/docheaders_list')
Sources = require('controllers/sources')
SourceEdit = require('controllers/source_edit')

class Main extends Spine.Stack
  controllers:
    sources: Sources
    documents: Documents
    sourceEdit: SourceEdit


  routes:
      '/source': 'sources'
      '/document': 'documents'
      '/sourceEdit/:id': 'sourceEdit'

module.exports = Main
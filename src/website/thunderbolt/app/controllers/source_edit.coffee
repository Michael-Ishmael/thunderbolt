Spine = require('spine')
Source = require('models/source')

class SourceEdit extends Spine.Controller
  className: 'sourceEdit'

  events:
    'submit form': 'submit'
    'click .save': 'submit'
    'click .delete': 'delete'

  elements:
    'form': 'form'

  constructor: ->
    super
    @active @change

  render: ->
      @html require('views/source_edit')(@item)

  change: (params) =>
      @item = Source.find(params.id)
      @render()

  submit: (e) ->
    e.preventDefault()
    @item.fromForm(@form).save()
    #@navigate('/contacts', @item.id)

  delete: ->
    @item.destroy() if confirm('Are you sure?')

    
module.exports = SourceEdit
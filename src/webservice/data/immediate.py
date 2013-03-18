import NeoData.DocumentRepository as pr
from entities.Document import Document
import simplejson as json

# docList = []
#
# for i in range(1, 11):
#     doc = Document()
#     doc.id = i
#     doc.title = 'Mr Fab' + str(i)
#     doc.sourceId = 24 + i
#     docList.append(doc.__dict__)
#
#
# print json.dumps(docList)

dr = pr.DocumentRepository()
dr.GetDocument(2)

__author__ = 'MichaelI'

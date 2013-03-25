from py2neo import rest, neo4j, cypher
from entities.CoreEntities import Document


class DocumentRepository():
    def __init__(self):
        self.uri = "http://localhost:7474/db/data/"

    def GetItems(self):
        m = lambda (d): d.__dict__
        return map(m, self.GetAllDocuments())

    def GetItem(self, id):
        return self.GetDocument(id).__dict__

    def GetGraphDb(self):
        return neo4j.GraphDatabaseService(self.uri)

    def GetAllDocuments(self):
        query = "START dn=node:references('id:2') MATCH (dn)-[:DOCUMENT]->(d) RETURN d"
        graph = self.GetGraphDb()
        results = cypher.execute(graph, query)
        docs = []
        for item in results[0]:
            doc = self.DocFromDataRec(item[0])
            docs.append(doc)

        return docs

    def GetDocument(self, id):
        query = "START dn=node:references('id:2') MATCH (dn)-[:DOCUMENT]->(d) WHERE d.id = {0} RETURN d".format(id)
        graph = self.GetGraphDb()
        results = cypher.execute(graph, query)
        docs = []
        if len(results) > 0 and len(results[0]) > 0 and len(results[0][0]) > 0:
            return self.DocFromDataRec(results[0][0][0])
        return None

    def DocFromDataRec(self, dbDoc):
        document = Document()
        document.id = dbDoc["id"]
        document.title = dbDoc["title"]
        document.date = dbDoc["date"]
        return document



__author__ = 'michaeli'

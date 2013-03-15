from py2neo import rest, neo4j, cypher


class DocumentRepository():
    def __init__(self):
        self.uri = "http://localhost:7474/db/data/"

    def GetGraphDb(self):
        return neo4j.GraphDatabaseService(self.uri)

    def GetAllDocuments(self):
        query = "START dn=node:references('id:2') MATCH (dn)-[:DOCUMENT]->(d) RETURN distinct d.title"
        graph = self.GetGraphDb()
        docs = cypher.execute(graph, query)
        for doc in docs:
            print(doc)


__author__ = 'michaeli'

__author__ = 'MichaelI'

import shutil
import subprocess
from py2neo import neo4j

neoPath = "C:\\michael\\local\pa\\"
uri = "http://localhost:7474/db/data/"


def getGraphDb():
    return neo4j.GraphDatabaseService(uri)


def createEntity(entity):
    graphDb = getGraphDb()
    refNode = graphDb.get_node(0)
    entityIndex = graphDb.get_or_create_index(neo4j.Node, entity["index"])
    newNode = graphDb.create( {"id":entity["id"], "title": entity["title"]})
    entityIndex.add("id", str(entity["id"]), newNode)
    entityIndex.add("reference", str(entity["title"]), newNode)
    graphDb.create((refNode, "REFERENCE", newNode))
    return newNode

def removeOldDb():
    shutil.rmtree(neoPath + "neoTest\\data")
    shutil.copytree(neoPath + "neoClean\\data", neoPath + "neoTest\\data")

def getRefNodes():
    refNodes = [{"id": 1, "title": "source", "index": "sources"}, {"id": 2, "title": "document", "index": "documents"},
                {"id": 3, "title": "author", "index": "authors"}, {"id": 4, "title": "category", "index": "categories"},
                {"id": 5, "title": "flag", "index": "flags"},
                {"id": 6, "title": "organisation", "index": "organisations"},
                {"id": 7, "title": "person", "index": "people"}, {"id": 8, "title": "country", "index": "countries"},
                {"id": 9, "title": "company", "index": "companies"}, {"id": 10, "title": "client", "index": "clients"},
                {"id": 11, "title": "agreement", "index": "agreements"}, {"id": 12, "title": "user", "index": "users"}]

    return refNodes

def setupRefNodes():
    refNodes = getRefNodes()
    for refNode in refNodes:
        createEntity(refNode)
    return None

def startNewDb():
    batFile = neoPath + "neoTest\\bin\\Neo4j.bat"
    subprocess.call([batFile])

removeOldDb()
startNewDb()
setupRefNodes()

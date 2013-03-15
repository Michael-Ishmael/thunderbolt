from py2neo import rest, neo4j

uri = "http://localhost:7474/db/data/"
publicationRefId = 0


def TestGraph():
    try:
        graph_db = neo4j.GraphDatabaseService(uri)
        print graph_db.neo4j_version
    except rest.NoResponse:
        print "Cannot connect to host"
    except rest.ResourceNotFound:
        print "Database service not found"


def CreatePublicationNodes():
    graph_db = neo4j.GraphDatabaseService(uri)
    #publicationRefNode = graph_db.create({"id": 1, "reference": "Source"})
    publicationRefNode = graph_db.get_node(1)
    publicationRefId = publicationRefNode.id
    references = graph_db.get_or_create_index(neo4j.Node, "references")
    references.add("reference", "source", publicationRefNode)
    references.add("id", 1, publicationRefNode)
    sources = graph_db.get_or_create_index(neo4j.Node, "sources")
    pub1, pub2, pub3 = graph_db.create({"id": 1, "title": "The Guardian", "readership": 204222, "pagerate": 3000},
                                       {"id": 2, "title": "The Times", "readership": 304222, "pagerate": 4000},
                                       {"id": 3, "title": "The Telegraph", "readership": 404222, "pagerate": 2500})
    sources.add("id", 1, pub1)
    sources.add("id", 2, pub2)
    sources.add("id", 3, pub3)

    publicationRefNode.create_relationship_to(pub1, "SOURCE")
    publicationRefNode.create_relationship_to(pub2, "SOURCE")
    publicationRefNode.create_relationship_to(pub3, "SOURCE")

    print(publicationRefId)


def CreateDocumentNodes():
    graph_db = neo4j.GraphDatabaseService(uri)
    sources = graph_db.get_or_create_index(neo4j.Node, "sources")
    documents = graph_db.get_or_create_index(neo4j.Node, "document")
    documentRefNode = graph_db.get_node(5)

    references = graph_db.get_or_create_index(neo4j.Node, "references")
    references.add("reference", "document", documentRefNode)
    references.add("id", 2, documentRefNode)

    doc1 = graph_db.get_node(6) #graph_db.create({"id": 1, "title": "Cameron gambles on MPs' vote over press regulation", "date": 20130314})
    doc2 = graph_db.get_node(7) #graph_db.create({"id": 2, "title": "Barack Obama seeks compromise with Republican senators", "date": 20130314})

    documents.add("id", 1, doc1)
    documents.add("id", 2, doc2)

    documentRefNode.create_relationship_to(doc1, "DOCUMENT")
    documentRefNode.create_relationship_to(doc1, "DOCUMENT")

    guardianNode = sources.get("id", 1)
    guardianNode.create_relationship_to(doc1, "PUBLISHED")
    guardianNode.create_relationship_to(doc2, "PUBLISHED")

    doc1.create_relationship_to(guardianNode, "PUBLISHED_BY")
    doc2.create_relationship_to(guardianNode, "PUBLISHED_BY")

__author__ = 'MichaelI'

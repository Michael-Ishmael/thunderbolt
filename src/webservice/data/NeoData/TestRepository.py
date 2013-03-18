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


def TestIndexAdd():
    graph_db = neo4j.GraphDatabaseService(uri)
    #references = graph_db.get_or_create_index(neo4j.Node, "references")
    references = graph_db.get_index(neo4j.Node, "references")
    documentRefNode = graph_db.create({"id":2, "reference":"document"})
    references.add("reference", "document", documentRefNode[0])
    references.add("id", 2, documentRefNode[0])

def CreateAuthorRef():
    graph_db = neo4j.GraphDatabaseService(uri)
    references = graph_db.get_or_create_index(neo4j.Node, "references")
    authorRefNode = graph_db.create({"id":3, "reference":"author"})[0]
    references.add("reference", "author",authorRefNode)
    references.add("id", 3, authorRefNode)


def CreateAuthor(jid, fName, lName, sourceId, docId):
    graph_db = neo4j.GraphDatabaseService(uri)
    references = graph_db.get_or_create_index(neo4j.Node, "references")
    sources = graph_db.get_or_create_index(neo4j.Node, "sources")
    authorsIndex = graph_db.get_or_create_index(neo4j.Node, "authors")
    documents = graph_db.get_or_create_index(neo4j.Node, "documents")

    authorRefNode = references.get("id", "3")[0]
    authors = graph_db.create({"id":jid, "firstname":fName, "lastname":lName, "title":"Journalist"})
                            #, {"id":2, "firstname":"Lisa", "lastname":"O'Carroll", "title":"Journalist"})

    authorRefNode.create_relationship_to(authors[0], "AUTHOR")
    #authorRefNode.create_relationship_to(authors[1], "AUTHOR")

    authorsIndex.add("id", jid, authors[0])
    #authorsIndex.add("id", 2, authors[1])

    sourceNode = sources.get("id", sourceId)[0]
    sourceNode.create_relationship_to(authors[0], "EMPLOYS")
    #guardianNode.create_relationship_to(authors[1], "EMPLOYS")

    authors[0].create_relationship_to(sourceNode, "WRITES_FOR")
    #authors[1].create_relationship_to(guardianNode, "WRITES_FOR")

    docNode = documents.get("id", docId)[0]
    docNode.create_relationship_to(authors[0], "WRITTEN_BY")
    #docNode.create_relationship_to(authors[1], "WRITTEN_BY")

    authors[0].create_relationship_to(docNode, "WROTE")
    #authors[1].create_relationship_to(docNode, "WROTE")

def CreateAuthors():
    CreateAuthor(4, "John-Paul", "Ford", "3", "3")
    CreateAuthor(5, "Hayley", "Dixon", "3", "4")

    CreateAuthor(6, "John-Paul", "Ford", "2", "5")
    CreateAuthor(7, "Hayley", "Dixon", "2", "6")

    #Patrick Wintour and Lisa O'Carroll = 1
    #Ewen MacAskill, Washington = 2
    #By John-Paul Ford Rojas10:15AM GMT 15 Mar 2013 =3
    #By Hayley Dixon 10:37AM GMT 15 Mar 2013 =4

    #Phillipe Naughton =5
    #Sadie Gray =6


def FixDocumentMapping():
    graph_db = neo4j.GraphDatabaseService(uri)
    documents = graph_db.get_or_create_index(neo4j.Node, "documents")
    references = graph_db.get_or_create_index(neo4j.Node, "references")
    documentRefNode = references.get("id", "2")[0]
    doc2 = documents.get("id", "2")[0]
    doc4 = documents.get("id", "4")[0]
    documentRefNode.create_relationship_to(doc2, "DOCUMENT")
    documentRefNode.create_relationship_to(doc4, "DOCUMENT")


def CreateDocumentNodes():
    graph_db = neo4j.GraphDatabaseService(uri)
    sources = graph_db.get_or_create_index(neo4j.Node, "sources")
    documents = graph_db.get_or_create_index(neo4j.Node, "documents")
    references = graph_db.get_or_create_index(neo4j.Node, "references")

    documentRefNode = references.get("id", "2")[0]

    doc1, doc2 = graph_db.create({"id": 5, "title": "MPs warned: Don't back 'state licensing of the press'", "date": 20130315},
                                     {"id": 6, "title": "Muslim convert Richard Dart admits terror charges", "date": 20130315})



    documents.add("id", 5, doc1)
    documents.add("id", 6, doc2)

    documentRefNode.create_relationship_to(doc1, "DOCUMENT")
    documentRefNode.create_relationship_to(doc2, "DOCUMENT")

    guardianNode = sources.get("id", "2")[0]
    guardianNode.create_relationship_to(doc1, "PUBLISHED")
    guardianNode.create_relationship_to(doc2, "PUBLISHED")

    doc1.create_relationship_to(guardianNode, "PUBLISHED_BY")
    doc2.create_relationship_to(guardianNode, "PUBLISHED_BY")

__author__ = 'MichaelI'




class Source:
    def __init__(self):
        self.id = -1
        self.title = ''
        self.readership = 0
        self.pageRate = 0


class Document:
    def __init__(self):
        self.id = -1
        self.title = ''
        self.date = 0
        self.sourceId = -1
        self.authorId = -1
        self.authorIds = []

    def mainAuthor(self):
        self.authorId = self.authorIds[0] if self.authorIds.length > 0 else -1
        return self.authorId

    def __str__(self):
        return "doc: id:{0}, title:{1}, date:{2}".format(self.id, self.title, self.date)



__author__ = 'funhead'

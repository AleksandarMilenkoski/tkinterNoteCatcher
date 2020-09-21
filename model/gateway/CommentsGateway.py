from model.table.CommentsTable import  CommentsTable
from model.domain.Comment import Comment

# newCommentsTable = CommentsTable()

class CommentsGateway:
    '''Comment Objects gateway'''
    def __init__(self, resource):
        self.resource = resource

    def getCommentById(self, id):
        data = self.resource.selectCommentById(id)
        return Comment(data[0], data[1])

    def getAllCommets(self):
        data = self.resource.selectAllComments()
        return self._dataListToObjectList(data)

    def getCommentsByLimit(self, limit):
        data = self.resource.selectCommentsByLimit(limit)
        return self._dataListToObjectList(data)

    def getCommentsByLimitOrderby(self, limit, order):
        data = self.resource.selectCommentByLimitOrderBy(limit, order)
        return self._dataListToObjectList(data)

    def getCommentsByPhrase(self, phrase):
        data = self.resource.selectCommentByPhrase(phrase)
        return self._dataListToObjectList(data)

    def getCommentByPhraseLimit(self, phrase, limit):
        data = self.resource.selectCommentByPhraseLimit(phrase, limit)
        return self._dataListToObjectList(data)

    def getCommentByPhraseLimitOrder(self, phrase, limit, order):
        data = self.resource.selectCommentByPhraseLimitOrder(phrase, limit, order)
        return self._dataListToObjectList(data)

    def addComment(self, obj):
        response = self.resource.insertComment(obj.getComment())
        obj.setId(response['id'])
        # print(obj.getId())

    def editComment(self, obj):
        self.resource.updateComment(obj.getId(), obj.getComment())

    def deleteComment(self, obj):
        self.resource.deleteComment(obj.getId())

    def _dataListToObjectList(self, dataList):
        objectsList = []
        for id, comment in dataList:
            objectsList.append(Comment(id, comment))

        return objectsList

# newCommentsGateway = CommentsGateway(CommentsTable())
# newCommentsGateway.getCommentsByLimit(5)
# print(newCommentsGateway.getCommentsByLimitOrderby(5, [('id', 'DESC')])[0].getId())
# newCommentsGateway.getCommentById(7)
# newCommentsGateway.getAllCommets()
# newCommentsGateway.getCommentsByPhrase('war')
# newCommentsGateway.getCommentByPhraseLimit('war', 5)
# newCommentsGateway.getCommentByPhraseLimitOrder('war', 5, [('id', 'DESC')])
# newCommentsGateway.addComment(Comment(None, 'nestoNovo'))
# newCommentsGateway.editComment(Comment(335, 'nestoNovoEdit'))
# newCommentsGateway.deleteComment(Comment(335, 'nestoNovoEdit'))

from model.table.TableAbstract import TableAbstract
import config

class CommentsTable(TableAbstract):
    """
        CommentsTable is a class for querying Comments Table
    """

    def __init__(self):
        super().__init__(config.DB_PATH)

    # def __init__(self):
    #     TableAbstract.__init__(self, config.DB_PATH)




    def selectAllComments(self):
        self.cursor.execute('''
			SELECT *
  			FROM comments;
			''')
        data = self.cursor.fetchall()

        return data

    def selectCommentsByLimit(self, limit):
        self.cursor.execute('''
			SELECT *
  			FROM comments
  			LIMIT ?;
			''', (limit,))
        data = self.cursor.fetchall()

        return data

    def selectCommentById(self, id):
        self.cursor.execute('''
			SELECT *
  			FROM comment
  			WHERE id=?;
			''', (id,))
        data = self.cursor.fetchone()
        return data

    def selectCommentByLimitOrderBy(self, limit, order, current_page):
        offset = (current_page - 1) * limit
        sql = '''
			SELECT *
			  FROM comments
			 ORDER BY {0}
			 LIMIT {1} OFFSET {2};
			 '''
        orderStr = self._generateOrderClause(order)

        # print(sql %(orderStr, limit))
        sql = sql.format(orderStr, str(limit), str(offset))

        # print(sql)
        # print(orderStr)

        # self.cursor.execute('''
        # 	SELECT *
        # 	  FROM comment
        # 	 ORDER BY id DESC
        # 	 LIMIT 5
        # ''')

        self.cursor.execute(sql)
        # self.cursor.execute('''
        # 	SELECT *
        # 	  FROM comment
        # 	 ORDER BY :orderStr
        # 	 LIMIT :limit;
        # ''', {
        # 		'orderStr': orderStr,
        # 		'limit': str(limit)
        # 		})

        data = self.cursor.fetchall()

        return data

    def selectCommentByPhrase(self, phrase):
        self.cursor.execute('''
			SELECT *
              FROM comments
             WHERE lower(comments.comment) LIKE ?
			''', ('%' + phrase.lower() + '%',))
        data = self.cursor.fetchall()

        return data

    def selectCommentByPhraseLimit(self, phrase, limit):
        self.cursor.execute('''
			SELECT *
              FROM comment
             WHERE lower(comment.comment) LIKE ?
             LIMIT ?
			''', ('%' + phrase.lower() + '%', limit, ))
        data = self.cursor.fetchall()

        return data

    def selectCommentByPhraseLimitOrder(self, phrase, limit, order):
        sql = '''
        			SELECT *
                      FROM comment
                     WHERE lower(comment.comment) LIKE {0}
                     ORDER BY {1}
                     LIMIT {2};
        			 '''
        orderStr = self._generateOrderClause(order)

        sql = sql.format(('"%' + phrase.lower() + '%"'), orderStr, str(limit))

        # print(sql)

        self.cursor.execute(sql)

        data = self.cursor.fetchall()

        return data

    def selectAllCommentsCount(self):
        self.cursor.execute('''
            SELECT count( * ) 
              FROM comments;
        ''')

        data = self.cursor.fetchone()[0]

        return data

    def insertComment(self, comment):
        self.cursor.execute('''
			INSERT INTO comment (
                        comment
                    )
                    VALUES (
                        ?
                    );
			''', (comment,))

        self.connection.commit()

        self.cursor.execute('''
			SELECT changes()
			''')

        data = self.cursor.fetchone()

        self.cursor.execute('''
        			SELECT last_insert_rowid();
        			''')
        newId = self.cursor.fetchone()

        return {
            'success': data[0],
            'id': newId[0]
        }

    def updateComment(self, id, comment):
        self.cursor.execute('''
			UPDATE comment
			   SET comment = :comment
			 WHERE comment.id = :id;
			''', {
            'id': id,
            'comment': comment
        })

        self.connection.commit()

        self.cursor.execute('''
			SELECT changes()
			''')

        data = self.cursor.fetchone()

        return data[0]

    def deleteComment(self, id):
        self.cursor.execute('''
			DELETE FROM comment
      		WHERE id = ?;
			''', (id,)
                            )

        self.connection.commit()

        self.cursor.execute('''
			SELECT changes()
			''')

        data = self.cursor.fetchone()

        return data[0]

    def _generateOrderClause(self, order):
        orderStr = ''
        for i, by in enumerate(order):
            field, direction = by
            orderStr += field + ' ' + direction
            if (i + 1) == len(order):
                break
            orderStr += ', '

        return orderStr


if __name__ == '__main__':

    newCommentsTable = CommentsTable()
    # print(newCommentsTable.selectAllComments())
    # print(newCommentsTable.selectCommentsByLimit(5))
    # print(newCommentsTable.selectCommentByLimitOrderBy(5, [('id', 'DESC')], 1))
    print(newCommentsTable.selectAllCommentsCount())
    # print(newCommentsTable.selectCommentByLimitOrderBy(5, [('id', 'DESC'), ('comment', 'DESC')]))
    # print(newCommentsTable.selectCommentById(7))
    # print(newCommentsTable.selectCommentByPhrase('Zion'))
    # print(newCommentsTable.selectCommentByPhraseLimit('Zion', 5))
    # print(newCommentsTable.selectCommentByPhraseLimitOrder('Zion', 5, [('id', 'DESC')]))
    # print(newCommentsTable.selectCommentByPhraseLimitOrder('Zion', 5, [('id', 'DESC'), ('comment', 'ASC')]))
    # print(newCommentsTable.insertComment('taman5'))
    # print(newCommentsTable.updateComment(329, 'nesto novo'))
    # print(newCommentsTable.deleteComment(329))

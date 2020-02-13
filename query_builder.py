from storage_client import ElasticBookStorage


class QueryBuilder(object):
    def __init__(self):
        self.client = ElasticBookStorage()

    def command(self, action, **kwargs):
        try:
            if action == 'append_book':

                self.client.create_book_doc(
                    title=kwargs['title'],
                    authors=kwargs['authors'],
                    summary=kwargs['summary'],
                    publisher=kwargs['publisher'],
                    num_reviews=kwargs['num_reviews'],
                    publish_date=kwargs['publish_date'],
                )

            elif action == 'retrieve_book_by_id':
                results = self.client.retrieve_book_by_id(book_id=kwargs['book_id'])
                return results
            elif action == 'remove_book_by_id':
                self.client.remove_book_doc(book_id=kwargs['book_id'])
        except Exception as ex:
            print(ex)

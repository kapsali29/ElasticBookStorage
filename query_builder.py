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
                results = 'Book created'

            elif action == 'retrieve_book_by_id':
                results = self.client.retrieve_book_by_id(book_id=kwargs['book_id'])

            elif action == 'remove_book_by_id':
                self.client.remove_book_doc(book_id=kwargs['book_id'])
                results = 'Book deleted'

            elif action == 'search_book_by_parameter':
                results = self.client.search_book_by_param(kwargs['term'], kwargs['query'])

            elif action == 'fuzzy_queries':
                results = self.client.fuzzy_queries(query=kwargs['query'], fields=kwargs['fields'])

            elif action == 'wild_card_query':
                results = self.client.wild_card_query(term=kwargs['term'], query=kwargs['query'])

            elif action == 'regex_query':
                results = self.client.regex_query(term=kwargs['term'], query=kwargs['query'])

            elif action == 'match_phrase_query':
                results = self.client.match_phrase_query(
                    query=kwargs['query'],
                    slop=kwargs['slop'],
                    fields=kwargs['fields']
                )

            elif action == 'match_phrase_prefix':
                results = self.client.match_phrase_prefix(query=kwargs['query'], slop=kwargs['slop'])

            elif action == 'term_query':
                results = self.client.term_query(field=kwargs['field'], term=kwargs['term'])

            return results
        except Exception as ex:
            print(ex)

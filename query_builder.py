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
                results = None

            elif action == 'retrieve_book_by_id':
                results = self.client.retrieve_book_by_id(book_id=kwargs['book_id'])

            elif action == 'remove_book_by_id':
                self.client.remove_book_doc(book_id=kwargs['book_id'])
                results = None

            elif action == 'search_book_by_parameter':
                results = self.client.search_book_by_param(kwargs['field'], kwargs['query'])

            elif action == 'fuzzy_queries':
                results = self.client.fuzzy_queries(query=kwargs['query'], fields=kwargs['fields'])

            elif action == 'wild_card_query':
                results = self.client.wild_card_query(field=kwargs['field'], query=kwargs['query'])

            elif action == 'regex_query':
                results = self.client.regex_query(field=kwargs['field'], query=kwargs['query'])

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

            elif action == 'delete_by_query':
                self.client.delete_by_query(fields=kwargs['fields'], query=kwargs['query'])
                results = None

            elif action == 'update_by_query':
                self.client.update_by_query(
                    fields=kwargs['fields'],
                    query=kwargs['query'],
                    field_to_update=kwargs['field_to_update'],
                    new_value=kwargs['new_value']
                )

            elif action == 'bool_query':
                results = self.client.query_combination(
                    should=kwargs['should'],
                    must=kwargs['must'],
                    must_not=kwargs['must_not']
                )

            return results
        except Exception as ex:
            print(ex)

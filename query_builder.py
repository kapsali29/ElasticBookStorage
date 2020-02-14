from storage_client import ElasticBookStorage


class QueryBuilder(object):
    def __init__(self):
        self.client = ElasticBookStorage()

    def get_source(self, results):
        """
        This function is used to get results from elasticsearch response

        :param results: elasticsearch response
        :return: json results

        Example:
            >>> builder = QueryBuilder()
            >>> json_results = builder.get_source(results)
        """
        if results:

            if isinstance(results, list):
                json_results = [book['_source'] for book in results]
                return json_results
            else:
                return results

    def command(self, action, payload):
        """
        This function is used to fetch elastic search results based on action parameter

        :param action: parameter
        :param payload: provided payload
        :return: result

        Example:
            >>> builder = QueryBuilder()
            >>> results = builder.command(action='fuzzy_queries', query='comprehesiv guide', fields=['title', 'summary'])
        """
        try:
            if action == 'append_book':

                self.client.create_book_doc(
                    title=payload['title'],
                    authors=payload['authors'],
                    summary=payload['summary'],
                    publisher=payload['publisher'],
                    num_reviews=payload['num_reviews'],
                    publish_date=payload['publish_date'],
                )
                results = None

            elif action == 'retrieve_book_by_id':
                results = self.client.retrieve_book_by_id(book_id=payload['book_id'])

            elif action == 'remove_book_by_id':
                self.client.remove_book_doc(book_id=payload['book_id'])
                results = None

            elif action == 'search_book_by_parameter':
                results = self.client.search_book_by_param(payload['field'], payload['query'])

            elif action == 'fuzzy_queries':
                results = self.client.fuzzy_queries(query=payload['query'], fields=payload['fields'])

            elif action == 'wild_card_query':
                results = self.client.wild_card_query(field=payload['field'], query=payload['query'])

            elif action == 'regex_query':
                results = self.client.regex_query(field=payload['field'], query=payload['query'])

            elif action == 'match_phrase_query':
                results = self.client.match_phrase_query(
                    query=payload['query'],
                    slop=payload['slop'],
                    fields=payload['fields']
                )

            elif action == 'match_phrase_prefix':
                results = self.client.match_phrase_prefix(query=payload['query'], slop=payload['slop'])

            elif action == 'term_query':
                results = self.client.term_query(field=payload['field'], term=payload['term'])

            elif action == 'delete_by_query':
                self.client.delete_by_query(fields=payload['fields'], query=payload['query'])
                results = None

            elif action == 'update_by_query':
                self.client.update_by_query(
                    fields=payload['fields'],
                    query=payload['query'],
                    field_to_update=payload['field_to_update'],
                    new_value=payload['new_value']
                )

            elif action == 'bool_query':
                results = self.client.query_combination(
                    should=payload['should'],
                    must=payload['must'],
                    must_not=payload['must_not']
                )

            return results
        except Exception as ex:
            print(ex)

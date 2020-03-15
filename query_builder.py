from storage_client import ElasticBookStorage
from utils import prepare_for_save, toJSON, save_json_to_file, save_attr_dict_to_csv


class QueryBuilder(object):
    def __init__(self):
        self.client = ElasticBookStorage()

    @staticmethod
    def get_source(results):
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
                return [results]

    @staticmethod
    def save_results(results, file_name, file_type):
        """
        This function saves elastic search results to file.
        The supported types are: csv, json, pickle

        :param results: elasticsearch results
        :param file_name: file name to store
        :param file_type: file type to store

        Example:
            >>> builder = QueryBuilder()
            >>> builder.save_results(results, "results", "csv")
        """
        prepared_data = prepare_for_save(results)  # modify actors field
        file = "{}.{}".format(file_name, file_type)

        if file_type == "json":
            jsonified_data = toJSON(prepared_data)  # jsonify data from ELK
            save_json_to_file(jsonified_data, file)

        elif file_type == "csv":
            save_attr_dict_to_csv(prepared_data, file)  # save data as CSV
        else:
            print("this type is not supported")

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
                results = self.client.delete_by_query(fields=payload['fields'], query=payload['query'])

            elif action == 'update_by_query':
                results = self.client.update_by_query(
                    fields=payload['fields'],
                    query=payload['query'],
                    field_to_update=payload['field_to_update'],
                    new_value=payload['new_value']
                )

            elif action == 'bool_query':

                data = dict()
                if 'should' in payload.keys():
                    data['should'] = payload['should']
                if 'must' in payload.keys():
                    data['must'] = payload['must']
                if 'must_not' in payload.keys():
                    data['must_not'] = payload['must_not']

                results = self.client.query_combination(**data)

            elif action == 'range_query':
                results = self.client.range_query(
                    field=payload['field'],
                    range=payload['range']
                )

            elif action == 'metric_aggregations':
                results = self.client.metric_aggregations(
                    field=payload['field'],
                    metric=payload['metric']
                )

            elif action == 'filter_aggregations':
                results = self.client.filter_aggregations(
                    term=payload['term'],
                    query=payload['query'],
                    metric=payload['metric'],
                    field=payload['field']
                )
            return results
        except Exception as ex:
            print(ex)

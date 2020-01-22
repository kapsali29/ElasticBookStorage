from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch_dsl import Search, Q

from settings import ELASTIC_INDEX, ELASTIC_DOC, ELASTIC_HOSTNAME, ELASTIC_PORT


# https://dzone.com/articles/23-useful-elasticsearch-example-queries

class ElasticBookStorage(object):

    def __init__(self):
        self.book_index = ELASTIC_INDEX
        self.book_doc = ELASTIC_DOC
        self.ELK_HOSTNAME = ELASTIC_HOSTNAME
        self.ELK_PORT = ELASTIC_PORT

        self.es = Elasticsearch([{
            'host': self.ELK_HOSTNAME,
            'port': self.ELK_PORT}]
        )

    def create_book_index(self):
        """
        The following function is used to create the book index
        :return: pass
        :Examples:
            >>> elk = ElasticBookStorage()
            >>> elk.create_book_index()
        """
        try:
            self.es.indices.create(index=self.book_index, ignore=400)
        except Exception as ex:
            print(ex)
        pass

    def bulk_insert(self, data):
        """
        The following function is used to insert bulk data to ElasticSearch

        :param data: list of dict
        :return:

        Example:
            >>> data = [{ "title": "Solr in Action", "authors": ["trey grainger", "timothy potter"], "summary" : "Comprehensive guide","publish_date" : "2015-12-03", "num_reviews": 18, "publisher": "manning" }]
            >>> bulk_insert(data)
        """
        try:
            actions = [
                {
                    "_index": self.book_index,
                    "_type": self.book_doc,
                    "_id": i,
                    "_source": data[i]
                }
                for i in range(len(data))
            ]
            helpers.bulk(self.es, actions=actions)
        except Exception as e:
            print(e)

    def create_book_doc(self, title, authors, summary, publisher, num_reviews, publish_date):
        """
        The following function is used to create a book entry to elasticsearch using the provided info
        :param title: book title
        :param authors: book authors
        :param summary: book summary
        :param publisher: book publisher
        :param num_reviews: book number of reviews
        :param publish_date: book publish date
        :return: pass

        :Example:
            >>> title="Some book"
            >>> authors=["Author1", "Author2"]
            >>> summary = "this is a book written by Author1 and Author2"
            >>> publisher = "Loki AE"
            >>> num_reviews = 20
            >>> publish_date = "2014-04-05"
            >>> elk = ElasticBookStorage()
            >>> elk.create_book_doc(title, authors, summary, publisher, num_reviews, publish_date)
        """
        try:
            body = {
                "title": title,
                "authors": authors,
                "summary": summary,
                "publisher": publisher,
                "num_reviews": num_reviews,
                "publish_date": publish_date
            }
            self.es.index(index=self.book_index, doc_type=self.book_doc, body=body)
        except Exception as e:
            print(e)

    def retrieve_book_by_id(self, book_id):
        """
        The following function is used to retrieve a book document from the elastic search using is ID
        :param book_id: book id
        :return: result document

        :Example:
            >>> elk = ElasticBookStorage()
            >>> book = elk.retrieve_book_by_id(book_id=2)
        """
        try:
            results = self.es.get_source(index=self.book_index, doc_type=self.book_doc, id=str(book_id))
            return results
        except Exception as ex:
            print(ex)

    def remove_book_doc(self, book_id):
        """
        The following function is used to remove a book entry from elastic search
        using its ID
        :param book_id: book ID
        :return:

        :Example:
            >>> elk = ElasticBookStorage()
            >>> elk.remove_book_doc(book_id=2)
        """
        try:
            self.es.delete(index=self.book_index, doc_type=self.book_doc, id=str(book_id))
        except Exception as e:
            print(e)

    def multi_match_query(self, query):
        """
        The following function is used to perform a basic match query using elastic search
        functionalities

        :param query: provided query parameter
        :return: results

        :Examples:
            >>> elk = ElasticBookStorage()
            >>> results = elk.basic_match_query(query="guide")
        """
        try:
            results = self.es.search(index=self.book_index, q=query)["hits"]["hits"]
            return results
        except Exception as e:
            print(e)

    def search_book_by_param(self, _source=[], *args):
        """
        The following function is used to retrieve results from
        elastic search searching for books that contains in their title

        the provided query
        :param query: provided query to search
        :return: results

        :Examples:
            >>> query = "in action"
            >>> elk = ElasticBookStorage()
            >>> results = elk.search_book_by_title("title", "in action")
        """
        try:
            term = args[0]
            query = args[1]

            body = {
                "query": {
                    "match": {
                        "{}".format(term): query
                    }
                },
                "_source": _source
            }
            results = self.es.search(index=self.book_index, body=body)["hits"]["hits"]
            return results
        except Exception as ee:
            print(ee)

    def fuzzy_queries(self, query, _source=[], **kwargs):
        """
        The following function receives a query and search to match books using the provided query
        to match books title and summary using Fuzzy matching.

        Fuzzy matching can be enabled on Match and Multi-Match queries to catch spelling errors.
        The degree of fuzziness is specified based on the Levenshtein distance from the original word,
        i.e. the number of one-character changes that need to be made to one string to make it the same
        as another string.

        :param query: provided query
        :return: results

        :Examples:
            >>> query="comprihensiv guide"
            >>> elk = ElasticBookStorage()
            >>> elk.fuzzy_queries(query, fields=["title", "summary"])
        """
        try:
            fields = kwargs["fields"]
            body = {
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": fields,
                        "fuzziness": "AUTO"
                    }
                },
                "_source": _source,
                "size": 1
            }

            results = self.es.search(index=self.book_index, body=body)["hits"]["hits"]
            return results
        except Exception as ee:
            print(ee)

    def wild_card_query(self, query, _source=[], *args):
        """
        This function is used to perform ElasticSearch wild card queries

        :param args: given arguments
        :param query: given query
        :return:

        Example:
            >>> wild_card_query("authors", query="t*")
        """
        try:
            field = args[0]

            body = {
                "query": {
                    "wildcard": {
                        "{}".format(field): query
                    }
                },
                "highlight": {
                    "fields": {
                        "".format(field): {}
                    }
                },
                "_source": _source
            }
            results = self.es.search(index=self.book_index, body=body)["hits"]["hits"]
            return results
        except Exception as ex:
            print(ex)

    def regex_query(self, query, _source=[], *args):
        """
        Regexp queries allow you to specify more complex patterns than wildcard queries

        :param query: provided query
        :param args: provided arguments
        :return:

        Example:
            >>> regex_query("authors", query="t[a-z]*y")
        """
        try:
            field = args[0]

            body = {
                "query": {
                    "regexp": {
                        "{}".format(field): query
                    }
                },
                "highlight": {
                    "fields": {
                        "{}".format(field): {}
                    }
                },
                "_source": _source
            }
            results = self.es.search(index=self.book_index, body=body)["hits"]["hits"]
            return results
        except Exception as ex:
            print(ex)

    def match_phrase_query(self, query, _source=[], **kwargs):
        """
        The match phrase query requires that all the terms in the query string be present in the document,
        be in the order specified in the query string and be close to each other.
        By default, the terms are required to be exactly beside each other but you can specify the slop value which
        indicates how far apart terms are allowed to be while still considering the document a match.

        :param query: provided query
        :param kwargs: provided kwargs
        :return:

        Example:
            >>> match_phrase_query(query="search engine", fields=["title", "summary"], slop=3, _source=[])
        """
        try:
            fields = kwargs["fields"]
            slop = kwargs["slop"]

            body = {
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": fields,
                        "type": "phrase",
                        "slop": slop
                    }
                },
                "_source": _source
            }
            results = self.es.search(index=self.book_index, body=body)["hits"]["hits"]
            return results
        except Exception as ex:
            print(ex)

    def match_phrase_prefix(self, query, slop, max_expansions=10, _source=[]):
        """
        Match phrase prefix queries provide search-as-you-type or a poor man’s version of autocomplete at query
        time without needing to prepare your data in any way.Like the match_phrase query,
        it accepts a slop parameter to make the word order and relative positions somewhat less rigid.
        It also accepts the max_expansions parameter to limit the number of terms matched in order to reduce resource intensity.

        :param query: provided query
        :param slop: provided slop
        :param max_expansions: provided max expansions
        :return:

        Example:
            >>> match_phrase_prefix(query="search en", slop=3)
        """
        try:
            body = {
                "query": {
                    "match_phrase_prefix": {
                        "summary": {
                            "query": query,
                            "slop": slop,
                            "max_expansions": max_expansions
                        }
                    }
                },
                "_source": _source
            }
            results = self.es.search(index=self.book_index, body=body)["hits"]["hits"]
            return results
        except Exception as ex:
            print(ex)

    def term_query(self, _source=[], **kwargs):
        """
        The above examples have been examples of full-text search.

        :param kwargs: provided kwargs
        :return:

        Example:
            >>> term_query(field="publisher", term="manning")
        """
        try:
            field = kwargs["field"]
            term = kwargs["term"]

            if isinstance(term, list):
                term_or_terms = "terms"
            else:
                term_or_terms = "term"

            body = {
                "query": {
                    "{}".format(term_or_terms): {
                        "{}".format(field): term
                    }
                },
                "_source": _source
            }
            results = self.es.search(index=self.book_index, body=body)["hits"]["hits"]
            return results
        except Exception as ex:
            print(ex)

    def delete_by_query(self, query, fields):
        """
        This function is used to delete by query

        :param query: provided query
        :param fields: provided fields
        :return:

        Example:
            >>> delete_by_query(query="python", fields=['title'])
        """
        try:
            client = Elasticsearch()
            s = Search(using=client, index=self.book_index)

            retrieved_items = s.query(
                Q("multi_match", query=query, fields=fields)
            )
            retrieved_items.delete()
        except Exception as ex:
            print(ex)

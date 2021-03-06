from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch_dsl import Search, Q, UpdateByQuery

from settings import ELASTIC_INDEX, ELASTIC_DOC, ELASTIC_HOSTNAME, ELASTIC_PORT, HITS_SIZE


# https://dzone.com/articles/23-useful-elasticsearch-example-queries

class ElasticBookStorage(object):

    def __init__(self):
        self.book_index = ELASTIC_INDEX
        self.book_doc = ELASTIC_DOC
        self.ELK_HOSTNAME = ELASTIC_HOSTNAME
        self.ELK_PORT = ELASTIC_PORT

        self.es = Elasticsearch([{
            'host': self.ELK_HOSTNAME,
            'port': self.ELK_PORT
        }])

    def create_book_index(self):
        """
        The following function is used to create the book index
        :return: pass
        :Examples:
            >>> elk = ElasticBookStorage()
            >>> elk.create_book_index()
        """
        try:
            body = {
                "mappings": {
                    "book_doc": {
                        "properties": {
                            "title": {
                                "type": "text"
                            },
                            "authors": {
                                "type": "text"
                            },
                            "summary": {
                                "type": "text"
                            },
                            "publish_date": {
                                "type": "date"
                            },
                            "num_reviews": {
                                "type": "integer"
                            },
                            "publisher": {
                                "type": "text"
                            }
                        }
                    }
                }
            }
            self.es.indices.create(index=self.book_index, body=body, ignore=400)
        except Exception as ex:
            print(ex, flush=True)
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
            print(e, flush=True)

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
            >>> publisher = "Publisher SA"
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
            print(e, flush=True)

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
            print(ex, flush=True)

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
            print(e, flush=True)

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
            results = self.es.search(index=self.book_index, q=query, size=HITS_SIZE)["hits"]["hits"]
            return results
        except Exception as e:
            print(e, flush=True)

    def search_book_by_param(self, *args, _source=[]):
        """
        The following function is used to retrieve results from
        elastic search searching for books that contains in their title

        the provided query
        :param _source: source argument
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
            results = self.es.search(index=self.book_index, body=body, size=HITS_SIZE)["hits"]["hits"]
            return results
        except Exception as ee:
            print(ee, flush=True)

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

            results = self.es.search(index=self.book_index, body=body, size=HITS_SIZE)["hits"]["hits"]
            return results
        except Exception as ee:
            print(ee, flush=True)

    def wild_card_query(self, _source=[], **kwargs):
        """
        This function is used to perform ElasticSearch wild card queries

        :param args: given arguments
        :param query: given query
        :return:

        Example:
            >>> wild_card_query(field="authors", query="t*")
        """
        try:
            field = kwargs['field']
            query = kwargs['query']

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
            results = self.es.search(index=self.book_index, body=body, size=HITS_SIZE)["hits"]["hits"]
            return results
        except Exception as ex:
            print(ex, flush=True)

    def regex_query(self, **kwargs):
        """
        Regexp queries allow you to specify more complex patterns than wildcard queries

        :param query: provided query
        :param args: provided arguments
        :return:

        Example:
            >>> regex_query("authors", query="t[a-z]*y")
        """
        try:
            field = kwargs['field'],
            query = kwargs['query']

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
            }
            results = self.es.search(index=self.book_index, body=body, size=HITS_SIZE)["hits"]["hits"]
            return results
        except Exception as ex:
            print(ex, flush=True)

    def match_phrase_query(self, query, **kwargs):
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
                "_source": []
            }
            results = self.es.search(index=self.book_index, body=body, size=HITS_SIZE)["hits"]["hits"]
            return results
        except Exception as ex:
            print(ex, flush=True)

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
            results = self.es.search(index=self.book_index, body=body, size=HITS_SIZE)["hits"]["hits"]
            return results
        except Exception as ex:
            print(ex, flush=True)

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
            results = self.es.search(index=self.book_index, body=body, size=HITS_SIZE)["hits"]["hits"]
            return results
        except Exception as ex:
            print(ex, flush=True)

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
            client = Elasticsearch(
                hosts=ELASTIC_HOSTNAME
            )
            s = Search(using=client, index=self.book_index)

            retrieved_items = s.query(
                Q("multi_match", query=query, fields=fields)
            )
            retrieved_items.delete()

            results = {'count': retrieved_items.count()}
            return results
        except Exception as ex:
            print(ex, flush=True)

    def update_by_query(self, **kwargs):
        """
        This function is used to update ElasticSearch entries by record

        :param kwargs: provided kwargs
        :return:

        Example:
            >>> update_by_query(fields="publisher", query="oreilly", field_to_update="publisher", new_value="OnMedia")
        """
        try:
            client = Elasticsearch(
                hosts=ELASTIC_HOSTNAME
            )
            ubq = UpdateByQuery(
                using=client,
                index=self.book_index
            )

            search_fields = kwargs["fields"]
            query = kwargs["query"]
            field_to_update = kwargs["field_to_update"]
            new_value = kwargs["new_value"]

            update_query = ubq.query(
                "multi_match",
                query=query,
                fields=search_fields
            ).script(
                source="ctx._source.{}='{}'".format(field_to_update, new_value)
            )
            results = update_query.execute()._d_
            return results
        except Exception as ex:
            print(ex, flush=True)

    def query_combination(self, **kwargs):
        """
        This function performs Combined bool queries

        :param kwargs: provided kwargs
        :return:

        Example:
            >>> should=[["title", "Elasticsearch"], ["title", "Solr"]],
            >>> must=[["authors", "clinton gormely"]],
            >>> must_not=[["authors", "radu george"]]
            >>> query_combination(should, must, must_not)

        """
        try:
            client = Elasticsearch(
                hosts=ELASTIC_HOSTNAME
            )

            s = Search(using=client, index=self.book_index)

            q = Q('bool',
                  must=[
                      Q({"multi_match": {"query": "{}".format(m[1]), "fields": ["{}".format(m[0])]}})
                      for m in kwargs["must"]] if "must" in kwargs.keys() else [],

                  should=[Q({"multi_match": {"query": "{}".format(m[1]), "fields": ["{}".format(m[0])]}})
                          for m in kwargs["should"]] if "should" in kwargs.keys() else [],

                  must_not=[Q({"multi_match": {"query": "{}".format(m[1]), "fields": ["{}".format(m[0])]}})
                            for m in kwargs["must_not"]] if "must_not" in kwargs.keys() else [],
                  minimum_should_match=1
                  )
            response = s.query(q).execute()["hits"]["hits"]
            return response.__dict__['_l_']

        except Exception as ex:
            print(ex, flush=True)

    def range_query(self, **kwargs):
        """
        The following function is used to fetch elastic search records based on range queries

        :param kwargs: provided kwargs
        :return: elastic search response

        Examples:
            >>> range_query(field='publish_date', range={"gte": "2015-01-01","lte": "2015-12-31"})
        """
        field = kwargs['field']
        ranges = kwargs['range']

        try:
            body = {
                "query": {
                    "range": {
                        "{}".format(field): ranges
                    }
                },
            }
            results = self.es.search(index=self.book_index, body=body, size=HITS_SIZE)["hits"]["hits"]
            return results
        except Exception as ex:
            print(ex, flush=True)

    def metric_aggregations(self, **kwargs):
        """
        The following function is used to return metric aggregations

        :param kwargs: provided kwargs
        :return: aggregated results

        Examples:
            >>> results = metric_aggregations(field='num_reviews', metric='min')
        """

        field = kwargs['field']
        metric = kwargs['metric']

        aggregation_name = "{}_{}".format(metric, field)

        try:
            body = {
                "aggs": {
                    "{}".format(aggregation_name): {
                        "{}".format(metric): {"field": field}
                    }
                }
            }

            results = self.es.search(index=self.book_index, body=body, size=0)["aggregations"]
            return results
        except Exception as ex:
            print(ex, flush=True)

    def filter_aggregations(self, **kwargs):
        """
        This function is used to aggregate data from elastic search using term query

        :param kwargs: provided kwargs
        :return: aggregated bucket data
        """

        term = kwargs['term']
        query = kwargs['query']
        field = kwargs['field']
        metric = kwargs['metric']

        try:

            body = {
                "aggs": {
                    "aggregated_data": {
                        "filter": {"term": {"{}".format(term): query}},
                        "aggs": {
                            "{}_{}".format(metric, field): {"{}".format(metric): {"field": field}}
                        }
                    }
                }
            }

            results = self.es.search(index=self.book_index, body=body, size=0)["aggregations"]
            return results
        except Exception as ex:
            print(ex, flush=True)

    def reviews_range_aggregation(self, **kwargs):
        """
        This function is used to fetch reviews aggregations from elastic search

        :param kwargs: provided kwargs
        :return: elastic search response

        Examples:
            >>> elk = ElasticBookStorage()
            >>> res = elk.reviews_range_aggregation(ranges=[{ "to" : 100 },{ "from" : 200 },{ "from" : 100, "to" : 200 }])
        """
        try:
            ranges = kwargs['ranges']

            body = {
                "aggs": {
                    "review_ranges": {
                        "range": {
                            "field": "num_reviews",
                            "ranges": ranges
                        }
                    }
                }
            }
            results = self.es.search(index=self.book_index, body=body, size=0)["aggregations"]
            return results
        except Exception as ex:
            print(ex, flush=True)

    def multi_get_books(self, **kwargs):
        """
        The following function is used to fetch books based on ElasticSearch mget API

        :param kwargs: provided kwargs
        :return: elastic search response

        Examples:
            >>> elk = ElasticBookStorage()
            >>> results = elk.multi_get_books(ids=[19,11])
        """
        try:
            book_ids = kwargs['ids']

            book_results = self.es.mget(
                index=self.book_index,
                doc_type=self.book_doc,
                body={'ids': book_ids},
            )
            book_docs = book_results['docs']
            results = {'docs': [book['_source'] for book in book_docs]}
            return results
        except Exception as ex:
            print(ex, flush=True)

    def get_cluster_health(self):
        """This function is used to retrieve cluster health info"""
        try:
            cluster_health = self.es.cluster.health()
            return cluster_health
        except Exception as ex:
            print(ex, flush=True)

    def get_cluster_stats(self):
        """This function is used to retrieve cluster stats info"""
        try:
            cluster_stats = self.es.cluster.stats()
            return cluster_stats
        except Exception as ex:
            print(ex, flush=True)

    def fetch_all_docs(self):
        """This function is used to returned all stored books"""
        try:
            body = {
                "query": {
                    "match_all": {}
                }
            }
            results = self.es.search(
                index=self.book_index,
                body=body,
                size=HITS_SIZE)["hits"]["hits"]
            return results
        except Exception as ex:
            print(ex, flush=True)

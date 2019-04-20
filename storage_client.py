from elasticsearch import Elasticsearch


class ElasticBookStorage(object):

    def __init__(self):
        self.book_index = "bookdb_index"
        self.book_doc = "book"
        self.ELK_HOSTNAME = "localhost"
        self.ELK_PORT = 9200

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

    def search_book_by_title(self, query):
        """
        The following function is used to retrieve results from
        elastic search searching for books that contains in their title

        the provided query
        :param query: provided query to search
        :return: results

        :Examples:
            >>> query = "in action"
            >>> elk = ElasticBookStorage()
            >>> results = elk.search_book_by_title(query)
        """
        try:
            body = {
                "query": {
                    "match": {
                        "title": query
                    }
                }
            }
            results = self.es.search(index=self.book_index, body=body)["hits"]["hits"]
            return results
        except Exception as ee:
            print(ee)

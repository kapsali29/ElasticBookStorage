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

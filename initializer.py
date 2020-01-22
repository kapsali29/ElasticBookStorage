#  This file is used to initialize ElasticSearch with Data
from storage_client import ElasticBookStorage

DATA = [
    {"title": "Elasticsearch: The Definitive Guide", "authors": ["clinton gormley", "zachary tong"],
     "summary": "A distibuted real-time search and analytics engine", "publish_date": "2015-02-07", "num_reviews": 20,
     "publisher": "oreilly"},
    {"title": "Taming Text: How to Find, Organize, and Manipulate It",
     "authors": ["grant ingersoll", "thomas morton", "drew farris"],
     "summary": "organize text using approaches such as full-text search, proper name recognition, clustering, tagging, information extraction, and summarization",
     "publish_date": "2013-01-24", "num_reviews": 12, "publisher": "manning"},
    {"title": "Elasticsearch in Action", "authors": ["radu gheorge", "matthew lee hinman", "roy russo"],
     "summary": "build scalable search applications using Elasticsearch without having to do complex low-level programming or understand advanced data science algorithms",
     "publish_date": "2015-12-03", "num_reviews": 18, "publisher": "manning"},
    {"title": "Solr in Action", "authors": ["trey grainger", "timothy potter"], "summary": "Comprehensive guide",
     "publish_date": "2015-12-03", "num_reviews": 18, "publisher": "manning"},
]

elk = ElasticBookStorage()
elk.create_book_index()

elk.bulk_insert(data=DATA)



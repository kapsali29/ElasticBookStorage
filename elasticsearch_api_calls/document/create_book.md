```
POST /book_index/book_doc
{
  "title": "Using ElasticSearch",
  "authors": ["George kibana"],
  "summary": "This is a guide how to use elasticsearch",
  "num_reviews":20,
  "publish_date":"2016-07-05",
  "publisher": "wiley"
}
```
response

```
{
  "_index" : "book_index",
  "_type" : "book_doc",
  "_id" : "NP30AnEBCps2865pSEdv",
  "_version" : 1,
  "result" : "created",
  "_shards" : {
    "total" : 2,
    "successful" : 1,
    "failed" : 0
  },
  "_seq_no" : 11,
  "_primary_term" : 1
}
```
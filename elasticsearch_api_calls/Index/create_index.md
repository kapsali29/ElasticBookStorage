```
PUT /book_index
{
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
            "type": "text"
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
```

response

```
{
  "acknowledged" : true,
  "shards_acknowledged" : true,
  "index" : "book_index"
}
```
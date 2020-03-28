```
POST /book_index/book_doc/_search
{
    "query": {
        "range" : {
            "publish_date": {
                "gte": "2016-01-01",
                "lte": "2016-12-31"
            }
        }
    }
}
```
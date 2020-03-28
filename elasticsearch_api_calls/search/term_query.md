```
POST /book_index/book_doc/_search
{
    "query": {
        "term" : {
            "publisher": "manning"
        }
    }
}
```
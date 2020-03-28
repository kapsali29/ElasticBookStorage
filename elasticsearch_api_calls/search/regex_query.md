```
POST /book_index/book_doc/_search
{
    "query": {
        "wildcard" : {
            "authors" : "t*"
        }
    }
}
```
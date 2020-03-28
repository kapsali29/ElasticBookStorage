```
POST /book_index/book_doc/_search
{
    "query": {
        "terms" : {
            "publisher": ["oreilly", "manning"]
        }
    }
}
```
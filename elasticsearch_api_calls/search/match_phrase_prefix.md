```
POST /book_index/book_doc/_search
{
    "query": {
        "match_phrase_prefix" : {
            "summary": {
                "query": "search en",
                "slop": 3,
                "max_expansions": 10
            }
        }
    }
}
```
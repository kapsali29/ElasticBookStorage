```
POST /book_index/book_doc/_search?size=0
{
    "aggs" : {
        "stats_reviews" : { "stats" : { "field" : "num_reviews" } }
    }
}
```
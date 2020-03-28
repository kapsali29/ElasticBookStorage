```
POST /book_index/book_doc/_search?size=0
{
    "aggs" : {
        "aggregated_data" : {
            "filter" : { "term": { "publisher": "wiley" } },
            "aggs" : {
                "stats_num_reviews" : { "stats": { "field" : "num_reviews" } }
            }
        }
    }
}
```
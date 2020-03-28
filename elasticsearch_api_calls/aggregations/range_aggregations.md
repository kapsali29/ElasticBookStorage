```
POST /book_index/book_doc/_search?size=0
{
    "aggs" : {
        "review_ranges" : {
            "range" : {
                "field" : "num_reviews",
                "ranges" : [
                    { "to" : 100.0 },
                    { "from" : 100.0, "to" : 200.0 },
                    { "from" : 200.0 }
                ]
            }
        }
    }
}
```
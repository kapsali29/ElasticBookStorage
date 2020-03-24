```
POST /book_index/book_doc/_search?size=1000
{
    "query": {
        "multi_match" : {
            "query" : "comprihensiv guide",
            "fields": ["title", "summary"],
            "fuzziness": "AUTO"
        }
    }
}
```
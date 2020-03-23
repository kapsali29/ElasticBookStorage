```
POST book_index/_update_by_query
{
  "query": {
    "multi_match": {
      "query": "wiley", 
      "fields": ["publisher"]
    }
  }, 
  "script": {"source": "ctx._source.publisher='Wiley Press'"}}
```
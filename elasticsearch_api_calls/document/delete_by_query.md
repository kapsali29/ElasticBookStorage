```
POST /book_index/_delete_by_query
{
  "query": {
    "match": {
      "title": "python"
    }
  }
}
```
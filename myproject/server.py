from elasticsearch import Elasticsearch
from bottle import route, run, request, template

es = Elasticsearch(['localhost:9200'])


@route('/')
def index():
    # / へのリクエストを処理

    # クエリの値を取得する
    query = request.query.q
    pages = search_pages(query) if query else []
    
    return template('search', query=query, pages=pages)


def search_pages(query):
    # 引数のクエリで Elasticsearch からページを検索し、結果のリストを返す

    result = es.search(index='pages', doc_type='page', body={
        "query": {
            "simple_query_string": {
                "query": query,
                "fields" : ["title=5", "content"],
                "default_operator": "and"
            }
        },
        "highlight": {
            "fields": {
                "content": {
                    "fragment_size": 150,
                    "number_of_fragments": 1,
                    "no_match_size": 150
                }
            }
        }
    })
    return result['hits']['hits']

if __name__ == '__main__':
    run(host='0.0.0.0', port=8000, debug=True, reloader=True)

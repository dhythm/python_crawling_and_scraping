import sys
import hashlib
import json


from elasticsearch import Elasticsearch

# クライアントを作成する
es = Elasticsearch(['localhost:9200'])

# pages インデックスを作成する
result = es.indices.create(index='pages', ignore=400, body={
    # kuromoji_analyzer を定義
    "settings": {
        "analysis": {
            "analyzer": {
                "kuromoji_analyzer": {
                    # 日本語形態素解析を使って文字列を分割する
                    "tokenizer" : "kuromoji_tokenizer"
                }
            }
        }
    },
    # page タイプを定義
    "mapppings": {
        "page": {
            "_all": {"analyzer": "kuromoji_analyzer"},
            "properties": {
                "url": {"type": "string"},
                "title": {"type": "string", "analyzer": "kuromoji_analyzer"},
                "content": {"type": "string", "analyzer": "kuromoji_analyzer"}
            }
        }
    }
})
print(result)

with open(sys.argv[1]) as f:
    for line in f:
        page = json.loads(line)
        # ドキュメントの ID を設定
        doc_id = hashlib.sha1(page['url'].encode('utf-8')).hexdigest()
        # Elasticsearch にインデックス化(保存)する
        result = es.index(index='pages', doc_type='page', id=doc_id, body=page)
        print(result)

import datetime

from elasticsearch import Elasticsearch

body = {"publishDate": datetime.datetime.now()}
host = ["http://172.10.11.69:9200/"]
es = Elasticsearch(host, verify_certs=True)

es.index(index='idy_recommend_index_data_test', doc_type='docs', refresh=True, body=body)
# es_search.index(index="idy_recommendtest", refresh=True, doc_type="docs", body=body)
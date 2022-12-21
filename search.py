from algoliasearch.search_client import SearchClient

client = SearchClient.create('QVBA9ZZPRA', '520ea8dd3ca37da55f2c5d86729b23a8')
index = client.init_index('KPMG_index')
# record = {"objectID": "200-2022-009993"}
# results = index.search(record)
res = index.get_object("200-2022-009993")
print(res["content"][0])
import flask
from flask import Flask, request, jsonify
import elasticsearch

app = Flask(__name__)

# Connect to elasticsearch
es = elasticsearch.Elasticsearch(['http://localhost:9200'])

# Indexing products
@app.route('/api/indexing_products', methods=['POST'])
def index_products():
    product_data = request.get_json()
    es.index(index='products', doc_type='product', body=product_data)
    return jsonify(success=True)

# Removing products
@app.route('/api/remove_products', methods=['POST'])
def remove_products():
    product_data = request.get_json()
    es.delete(index='products', doc_type='product', id=product_data['id'])
    return jsonify(success=True)

# Updating products
@app.route('/api/update_products', methods=['POST'])
def update_products():
    product_data = request.get_json()
    es.update(index='products', doc_type='product', id=product_data['id'], body=product_data)
    return jsonify(success=True)

# Searching products
@app.route('/api/search_products', methods=['GET'])
def search_products():
    query = request.args.get('query')
    res = es.search(index='products', body={"query": query})
    return jsonify(res['hits']['hits'])

if __name__ == '__main__':
    app.run()
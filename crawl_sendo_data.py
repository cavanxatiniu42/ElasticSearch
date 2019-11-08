from elasticsearch import Elasticsearch
import requests
import json

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache"
    }

def check_if_index_is_exist(url):
    response = requests.get(url)
    json_data = response.json()
    return json_data


def create_mapping():
    url = "http://localhost:9200/_template/search_engine_template/"
    response = requests.request("GET", url, data="")
    if len(response.text) > 2:
        print("1. Deleted template: search_engine_template")
        response_delete = requests.delete(url)
    template = {
        'template': {
            'setting': {
                'number_of_shards': 1
            },
            'mapping': {
                'men-wears': {
                    '_source': {
                        'entable': True
                    }
                },
                'properties': {
                    'name': {
                        'type': 'text',
                        'index': True
                    },
                    'price': {
                        'type': 'integer',
                        'index': True
                    },
                    'image': {
                        'type': 'text'
                    }
                }
            }
        }
    }
    template = json.dumps(template)
    response = requests.put(url, data=template, headers=headers)
    if response.status_code == 200:
        print('create mapping template')



def create_men_wears_index():
    url = 'http://localhost:9200/men-wears'
    json_data = check_if_index_is_exist(url)
    if 'error' not in json_data:
        requests.delete(url)
    response = requests.put(url)
    if response.status_code == 200:
        print('create men-wears index')


def crawl_sendo_data():
    url = 'https://www.sendo.vn/m/wap_v2/category/product?category_id=94&listing_algo=algo5&p=1&platform=web&s=60&sortType=vasup_desc'
    url_r = requests.get(url)
    raw_data = url_r.json()['result']['data']
    for i, product in enumerate(raw_data):
        product_body = {
            'name': product['name'],
            'price': product['price'],
            'image': product['image']
        }

        res = es.index(index='men-wears', doc_type='maleswear', id=i, body=product_body)
    return res


if __name__ == '__main__':
    create_mapping()
    create_men_wears_index()
    crawl_sendo_data()
    # res = es.search(index='men-wears', body={'query': {'match': {'name': 'QUẦN TÂY NAM ỐNG CÔN VẢI CO DÃN'}}})
    # print(res)

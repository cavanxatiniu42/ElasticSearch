from flask import Flask, render_template, request, redirect, url_for
from elasticsearch import Elasticsearch
import re
import requests
import json

app = Flask(__name__)
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def get_search_infomation():
    if request.method == 'POST':
        search_term = request.form['name']
        price = request.form.get('price')

        if search_term and not price:
            return redirect(url_for('search_by_name_description', search_term=search_term))
        if price:
            if '&' in price:
                price_range = price.split('&')
                gtprice = re.findall('\\d+', price_range[0])[0]
                ltprice = re.findall('\\d+', price_range[1])[0]
            else:
                if 'gt' in price:
                    gtprice = re.findall('\\d+', price)[0]
                    ltprice = 0
                if 'lt' in price:
                    gtprice = 0
                    ltprice = re.findall('\\d+', price)[0]
            if price and not search_term:
                return redirect(url_for('search_by_price', gtprice=gtprice, ltprice=ltprice))
            if price and search_term:
                return redirect(
                    url_for('search_by_name_price', search_term=search_term, gtprice=gtprice, ltprice=ltprice))


@app.route('/search_result_by_name', methods=['POST', 'GET'])
def search_by_name_description():
    search_term = request.args.get('search_term')
    body = {
        'query': {
            'bool': {
                'must': {
                    'match': {
                        'name': search_term
                    }
                }
            }
        }
    }
    result = es.search(index='men-wears', body=body)['hits']['hits']
    return render_template('result_page.html', result=result)


@app.route('/search_result_by_price', methods=['GET', 'POST'])
def search_by_price():
    gtprice = request.args.get('gtprice')
    ltprice = request.args.get('ltprice')
    body = {}
    if gtprice != 0 and ltprice != 0:
        body = {
            'query': {
                'range': {
                    'price': {
                        'gte': gtprice + '000',
                        'lte': ltprice + '000',
                    }
                }
            }
        }
    elif gtprice == 0:
        body = {
            'query': {
                'range': {
                    'price': {
                        'lte': ltprice + '000'
                    }
                }
            }
        }
    elif ltprice == 0:
        body = {
            'query': {
                'range': {
                    'price': {
                        'gte': gtprice + '000'
                    }
                }
            }
        }

    result = es.search(index='men-wears', body=body)['hits']['hits']
    return render_template('result_page.html', result=result)


@app.route('/search_by_name_price')
def search_by_name_price():
    gtprice = request.args.get('gtprice')
    ltprice = request.args.get('ltprice')
    search_term = request.args.get('search_term')
    body = {}
    if gtprice != 0 and ltprice != 0:
        body = {
            'query': {
                'bool': {
                    'must': {
                        'match': {
                            'name': search_term
                        }
                    },

                    'filter': {
                        'range': {
                            'price': {
                                'gte': gtprice + '000',
                                'lte': ltprice + '000',
                            }
                        }
                    }
                }
            }
        }
    elif gtprice == 0:
        body = {
            'query': {
                'bool': {
                    'must': {
                        'match': {
                            'name': search_term
                        }
                    },

                    'filter': {
                        'range': {
                            'price': {
                                'lte': ltprice + '000'
                            }
                        }
                    }
                }
            }
        }
    elif ltprice == 0:
        body = {
            'query': {
                'bool': {
                    'must': {
                        'match': {
                            'name': search_term
                        }
                    },

                    'filter': {
                        'range': {
                            'price': {
                                'gte': gtprice + '000',
                            }
                        }
                    }
                }
            }
        }

    result = es.search(index='men-wears', body=body)['hits']['hits']
    return render_template('result_page.html', result=result)


if __name__ == '__main__':
    app.run("0.0.0.0", port=8005, debug=True, threaded=True)

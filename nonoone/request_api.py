import requests
import json
import locale
import random
from pymongo import MongoClient
from pprint import pprint

host_thuannh =  "http://192.168.10.148:8000"
host_db = "mongodb://192.168.10.127:27017"
host_thuandh = "http://192.168.10.127:5010/"

def get_response_recommend_size(message = "45 - 20 - 41 - 40 - 66"):

    data = {'size': message}
    # data = "{'size':'" +message+"'}"
    response = requests.post(host_thuannh + "/api/infer", data=data)
    #                         headers={'content-Type':'application/json'})
    # print(response.text)
    tmps = json.loads(response.text)
    # print(tmps['url'])

    return tmps['url']

def get_recommend_size():

    # data = {}
    url = host_thuannh + "/recommend/recommend_size1.jpg"

    return url

colors_map = {
    'BL':'đen',
    'BB': 'xanh',
    'BU': 'đỏ',
    'DG': 'đen',
    'DH': 'xám',
    'DR': 'đỏ',
    'EC': 'trắng',
    'EG': 'đen',
    'KG': 'xanh',
    'LB': 'trắng',
    'LG': 'xanh',
    'GY': 'xanh',
    'MGY': 'xám',
    'MWH': 'trắng',
    'MO': 'đen',
    'NA': 'đen',
    'OR': 'cam',
    'RE': 'đỏ',
    'WH': 'trắng'
}
def map_colors(color):

    tmps = []
    # print(color)
    for key, value in colors_map.items():
        if value == color:
            tmps.append(key)

    return tmps


def format_currency(num):
    locale.setlocale(locale.LC_ALL, 'vi_VN')
    return locale.currency(num, grouping=True)

def random_price():
    price = format_currency((random.randint(5, 30) + 5) * 10000)
    return price

username = "root"
password = "example"

def get_clothes_recommend(gender="nam", color="trắng", type_item="phông"):

    client = MongoClient(host_db, username=username, password=password)
    db = client.Fashion
    color_code = map_colors(color)
    # print(color)
    pipeline = [
        {'$match':
             {'$and':[
                 {'is_try': 1},
                 {'color_code': {'$in': color_code}},
             ]}},
        {'$limit': 50},
        {'$project':{
            'name': 1,
            'image_path': 1,
        }}
    ]

    items = db.search_collection.aggregate(pipeline)

    iitems = []
    url_clothes = []
    for item in items:
        tmp = host_thuandh + item['image_path']
        # print(tmp)
        url_clothes.append(tmp)

    return url_clothes

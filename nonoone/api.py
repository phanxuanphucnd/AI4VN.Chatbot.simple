import requests
import json
from pymongo import MongoClient
from pprint import pprint

# message = "47 - 23 - 44 - 45 - 68"
def get_response_recommend_size(message = "45 - 20 - 41 - 40 - 66"):

    data = {'size': message}
    # data = "{'size':'" +message+"'}"
    response = requests.post("http://192.168.10.148:8000/api/infer", data=json.dumps(data),\
                             headers={'content-Type':'application/json'})
    tmps = json.loads(response.text)
    print(tmps['url'])

    return tmps['url']

# res = get_response_recommend_size(message)
# print(type(res))
# pprint(res)

def get__recommend_size():

    # data = {}
    url = "http://192.168.10.148:8000/recommend/recommend_size1.png"

    return url

# color = 'trang'
def map_color(color="den"):
    maps = {'do': 'đỏ',
            'đỏ': 'đỏ',
            'vang': 'vàng',
            'vàng': 'vàng',
            'hồng': 'hồng',
            'hong': 'hồng',
            'đen': 'đen',
            'den': 'đen',
            'trang': 'trắng',
            'trắng': 'trắng',
            'Do': 'đỏ',
            'Đỏ': 'đỏ',
            'Vang': 'vàng',
            'Vàng': 'vàng',
            'Hồng': 'hồng',
            'Hong': 'hồng',
            'Đen': 'đen',
            'Den': 'đen',
            'Trang': 'trắng',
            'Trắng': 'trắng'
            }
    return maps[color]
# print(map_color(color))

def map_cat(cat="phong"):
    maps = {'phong': 'phông',
            'phông': 'phông',
            'Phong': 'phông',
            'Phông': 'phông',
            'the thao': 'thể thao',
            'thể thao': 'thể thao',
            'The thao': 'thể thao',
            'Thể thao': 'thể thao',
            'sơ mi': 'sơ mi',
            'so mi': 'sơ mi',
            'Sơ mi': 'sơ mi',
            'So mi': 'sơ mi'
            }
    return maps[cat]

def get_recommend_clothes(gender="nam", color="đen", type_item="phông"):

    if gender.lower() == "nam":
        mgender = '0'
    else:
        mgender = '1'
    mcolor = map_color(color)
    mcat = map_cat(type_item)
    params = {}
    if type_item != None:
        params['cat'] = mcat
    if gender != None:
        params['gender'] = mgender
    if color != None:
        params['color'] = mcolor

    response = requests.get(url="http://192.168.0.104:5000/filter", params=params)
    tmps = json.loads(response.text)

    return tmps

# res = get_recommend_clothes()
# pprint(res)


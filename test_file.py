import requests
import json
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Mở và đọc tệp JSON với mã hóa đúng
with open('category.json', 'r', encoding='utf-8', errors='ignore') as file:
    category = json.load(file)
# Encoding = utf8 để có tiếng việt
sys.stdout.reconfigure(encoding='utf-8')

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Access-Control-Allow-Origin': '*',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Origin': 'https://www.bachhoaxanh.com',
    'Referer': 'https://www.bachhoaxanh.com/thit-heo',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
    'authorization': 'Bearer 38588F2C69DD9527E6E138B53A46B610',
    'deviceid': 'bcccec6e-1af3-4a6b-a216-4649fed3bb74',
    'platform': 'webnew',
    'referer-url': 'https://www.bachhoaxanh.com/thit-heo',
    'reversehost': 'http://bhxapi.live',
    'sec-ch-ua': '"Chromium";v="130", "Microsoft Edge";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'xapikey': 'bhx-api-core-2022',
}

page_index = 1
all_products = []
while True:
    json_data = {
        'provinceId': 3,
        'wardId': 0,
        'districtId': 0,
        'storeId': 7300,
        'CategoryId': 8781,
        'SelectedBrandId': '',
        'PropertyIdList': '',
        'PageIndex': page_index,
        'PageSize': 10,
        'SortStr': '',
        'PriorityProductIds': '226834,275804,275806,314535,233760,233783,233758,249012,226937,226856,233756,249011,238781,226865,226842,233782,233789,233766,249017,297342,232832',
        'PropertySelected': [],
        'LastShowProductId': 233756,
    }

    try:
        response = requests.post('https://apibhx.tgdd.vn/Category/AjaxProduct', headers=headers, json=json_data)
        
        if response.status_code != 200:
            print(f"Lỗi từ máy chủ: {response.status_code}")
            print(response.text)
            break
        
        response_json = response.json()

        try:
            all_products.extend(response_json["data"]["products"])
        except KeyError:
            print(f"Trang {page_index} không có dữ liệu sản phẩm.")
            break
        
        page_index += 1
        
        if len(response_json["data"]["products"]) < json_data["PageSize"]:
            break
        
    except KeyError as e:
        print(f"Lỗi KeyError: {e}")
        break
    except json.JSONDecodeError as e:
        print(f"Lỗi JSONDecodeError: {e}")
        break
    except requests.exceptions.RequestException as e:
        print(f"Lỗi yêu cầu: {e}")
        break

# In thông tin tất cả các sản phẩm
for product in all_products:
    print(f'ID: {product["id"]}, Tên: {product["name"]}, Số lượng: {product["productPrices"][0]["quantity"]}, Giá: {product["productPrices"][0]["price"]}')

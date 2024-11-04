import requests
import json
import pandas as pd
import sys
import time
import random

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
    'Origin': 'https://www.bachhoaxanh.com',
    'Referer': 'https://www.bachhoaxanh.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'authorization': 'Bearer 3F7BA52523D9989458020E0F1E272720',
    'deviceid': '6139e2b8-d41f-4b45-9a61-c1ce300a81e8',
    'platform': 'webnew',
    'referer-url': 'https://www.bachhoaxanh.com/',
    'reversehost': 'http://bhxapi.live',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'xapikey': 'bhx-api-core-2022',
}


# Duyệt qua từng mục trong category để lấy CategoryId
Page_index = 1 
for id_key in category:
    try:
        category_id = int(id_key["id"])
        # Lặp để duyệt qua các trang Pageindex trong 1 mục
        while 1:
            json_data = {
                'provinceId': 3,
                'wardId': 0,
                'districtId': 0,
                'storeId': 7300,
                'CategoryId': category_id,
                'SelectedBrandId': '',
                'PropertyIdList': '',
                'PageIndex': Page_index,
                'PageSize': 10,
                'SortStr': '',
                'PriorityProductIds': '226834,275804,275806,314535,233760,233783,233758,249012,226937,226856,233756,249011,238781,226865,226842,233782,233789,233766,249017,297342,232832',
                'PropertySelected': [],
                'LastShowProductId': 233756,
            }
            
            response = requests.post('https://apibhx.tgdd.vn/Category/AjaxProduct', headers=headers, json=json_data)
            
            #Đổi thành file Json để đọc và lấy dữ liệu
            response_json = response.json()

            Page_index += 1
        print(category["name"]) 
        print(response.text)
        # Nếu độ dài sản phẩm của 1 mục nhỏ hơn PageSize thì thoát vòng lặp
        if len(response_json["data"]["products"]) < json_data["PageSize"]:
                break
    except ValueError:
        print(f"Bỏ qua giá trị id không hợp lệ: {id_key['id']}")


all_filtered_data = []

print(response.text)
response_json = response.json()
print(response_json)
if "data" in response_json:
    for product in response_json["data"]["products"]:
        product_id = product["id"]
        product_name = product["name"]
        quantity = product["productPrices"][0]["quantity"]
        price = product["productPrices"][0]["price"]
        all_filtered_data.append([product_id, product_name, quantity, price])

    df = pd.DataFrame(all_filtered_data, columns=["ID", "Tên Sản Phẩm", "Số Lượng", "Giá"])
    df.to_excel("products.xlsx", index=False)

print("Đã lưu tất cả dữ liệu vào file products.xlsx")

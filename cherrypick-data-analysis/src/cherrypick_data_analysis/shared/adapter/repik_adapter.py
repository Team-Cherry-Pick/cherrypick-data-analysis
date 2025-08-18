import requests

from shared.config.env import *


def upload_deal(deal) :
    if deal["shipping_type"] != "FREE" :
        print("무료배송이 아닙니다.")
        return

    response = upload_prod_server(deal)
    upload_dev_server(deal)

    if response.status_code != 200 :
        print(f"{response.status_code} : response {response.text}")
        return None
    else :
        print(f"{response.status_code} : response {response.json()}")
        return deal["title"]

def upload_dev_server(deal)  :
    response = requests.post(
        DEV_POST_DEAL_URL,
        headers={"Authorization": f"Bearer {DEV_REPIK_TOKEN}"},  # Authorization 헤더는 보통 대문자로
        json={  # 중첩된 데이터는 json=으로
            "title": deal["title"],
            "categoryId": deal["category_id"],
            "imageIds": [-1],
            "originalUrl": deal["url"],
            "storeId": deal["store_id"],
            "storeName": deal["store_name"],
            "price": {
                "priceType": "KRW",
                "regularPrice": deal["origin_price"],
                "discountedPrice": deal["discounted_price"]
            },
            "shipping": {
                "shippingType": deal["shipping_type"],
                "shippingPrice": 0,
                "shippingRule": ""
            },
            "content": deal["content"]
        }
    )
    return response

def upload_prod_server(deal)  :
    response = requests.post(
        PROD_POST_DEAL_URL,
        headers={"Authorization": f"Bearer {PROD_REPIK_TOKEN}"},  # Authorization 헤더는 보통 대문자로
        json={  # 중첩된 데이터는 json=으로
            "title": deal["title"],
            "categoryId": deal["category_id"],
            "imageIds": [deal["image_id"]],
            "originalUrl": deal["url"],
            "storeId": deal["store_id"],
            "storeName": deal["store_name"],
            "price": {
                "priceType": "KRW",
                "regularPrice": deal["origin_price"],
                "discountedPrice": deal["discounted_price"]
            },
            "shipping": {
                "shippingType": deal["shipping_type"],
                "shippingPrice": 0,
                "shippingRule": ""
            },
            "content": deal["content"]
        }
    )
    return response


def request_deal_info(url:str) :
    resp = requests.get(f"{DEAL_INFO_URL}?url={url}")

    if resp.status_code != 200 :
        raise Exception(f"{resp.status_code}{resp.text}")

    return resp.json()


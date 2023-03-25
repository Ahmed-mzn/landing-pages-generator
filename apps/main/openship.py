import requests
from decouple import config
import uuid


def create_user(name, email, password, business_name):
    query = """
        mutation {
          createUser(
            data: {
                name: """+f'"{name}"'+"""
                email: """+f'"{email}"'+"""
                password: """+f'"{password}"'+"""
            }
          ){
            id
            name
            email
          }
        }
    """

    token = config('OPENSHIP_TOKEN')
    headers = {"x-api-key": f"{token}"}

    endpoint = "https://khaled.myopenship.com/api/graphql"
    r = requests.post(endpoint, json={"query": query}, headers=headers)
    res_json = r.json()
    user_id = res_json['data']['createUser']['id']

    create_shop(user_id, business_name)


def create_shop(user_id, shop_name):
    query = """
        mutation {
          createShop(
            data: {
                name: """ + f'"{shop_name}"' + """
                domain: """ + f'"{str(uuid.uuid4())}.sfhat.io"' + """
                type: "custom"
                user: {
                    connect: {
                        id: """ + f'"{user_id}"' + """
                    }
                }
            }
          ){
            id
            name
          }
        }
    """
    token = config('OPENSHIP_TOKEN')
    headers = {"x-api-key": f"{token}"}

    endpoint = "https://khaled.myopenship.com/api/graphql"
    r = requests.post(endpoint, json={"query": query}, headers=headers)


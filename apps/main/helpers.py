import requests

# token = "Fe26.2**a9f5baec0ae079c17b5c3583b997a216d6a69ff491a7863f29484d2426c47e99*E6XjXTZ-YO3m6LCmoMkZ8w*gNoljckWdNDqfOhgFau_3gBd2wEqTn-GhtDGy4bXKrb8cOuU8TdeYjJ7rTH_NBhdhROv7TsKffqt7xqKxjyyfw*1679598466295*222862d126b2d9575e7877561a11233162fc9692c4a0b9c1152e5f726d9b5659*z16BBlre7QwBbhpHMv8OsVUOw7WyUfn8VfSb4aSvNLY"
# apiKey = "cleekks4o03790umc4rid5f9i"
# headers = {"Authorization": f"Bearer {token}"}
# query = """
# query {
#     users{
#         name,
#         email
#     }
# }
# """



# endpoint = "https://khaled.myopenship.com/api/graphql"
# r = requests.post(endpoint, json={"query": query}, headers=headers)
#
# print(r.json())

import json
import os


def search_ar(data, query):
    for item in data:
        if item["city_ar"] == query:
            return item["city_en"]
    return ""


def search_en(data, query):
    for item in data:
        if item["city_en"] == query:
            return item["city_ar"]
    return ""


def check(data, pk):
    for item in data:
        if item["id"] == pk:
            return True
    return False


def best():
    module_dir = os.path.dirname(__file__)

    f_test = open(os.path.join(module_dir, "aymakan_test.json"), encoding='utf-8')
    data_test = json.load(f_test)
    i = 0
    # for item in data_test:
    #     if "success" in item:
    #         i += 1
    #         print(item["shipping"]["tracking_number"])
    #         print("ok")
    # print(i)
    # f_main = open(os.path.join(module_dir, "main.json"), encoding='utf-8')
    # data_main = json.load(f_main)
    #
    # f_salla = open(os.path.join(module_dir, "salla.json"), encoding='utf-8')
    # data_salla = json.load(f_salla)
    #
    # f_aymakan = open(os.path.join(module_dir, "aymakan.json"), encoding='utf-8')
    # data_aymakan = json.load(f_aymakan)

    # for item in data_salla:
    #     if item["aymakan_ar"] == "":
    #         item["aymakan_ar"] = search_en(data_aymakan, item["name_en"])
    #
    # for item in data_salla:
    #     if item["aymakan_en"] == "":
    #         item["aymakan_en"] = search_ar(data_aymakan, item["name"])

    # print(data_salla)
    # with open('test.json', 'w', encoding='utf-8') as json_file:
    #     json.dump(data_salla, json_file)
    # new_data = []
    # for item in data_salla:
    #     is_here = check(data_main, item["id"])
    #     if not is_here:
    #         new_data.append(item)
    #
    # f_salla.close()
    # f_aymakan.close()
    # return new_data


import zeep

# wsdl = 'https://track.smsaexpress.com/SECOM/SMSAwebService.asmx?wsdl'
# client = zeep.Client(wsdl=wsdl)
# res = client.service.cancelShipment('290442697317', 'Testing2', 'delete')
# res = client.service.getTracking('290442697317', 'Testing2')['_value_1']['_value_1']

# res = client.service.getPDF('290442697317', 'Testing2')
# print(res)



# track
# wsdl = 'https://track.smsaexpress.com/SECOM/SMSAwebService.asmx?wsdl'
# client = zeep.Client(wsdl=wsdl)
#
# response = client.service.getTracking(self.order.shipping_tracking_id, self.pass_key)
# print(response)

# for item in response['_value_1']['_value_1']:
#     tracking_info.append({
#         'code': 'cancelled' if item['Tracking']['Activity'] == 'CANCELLED ON CLIENTS REQUEST' else item['Tracking']['Activity'],
#         'description': item['Tracking']['Details'],
#         'created_at': item['Tracking']['Date']
#     })
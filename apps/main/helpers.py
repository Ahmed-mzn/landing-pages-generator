
# total = 10
# percentage = 30
# value = round((27/100) * total)
# value2 = round((30/100) * total)
# value3 = round((40/100) * total)
#
# print(f"res: {value}")
# print(f"res2: {value2}")
# print(f"res3: {value3}")


import requests

token = "Fe26.2**a9f5baec0ae079c17b5c3583b997a216d6a69ff491a7863f29484d2426c47e99*E6XjXTZ-YO3m6LCmoMkZ8w*gNoljckWdNDqfOhgFau_3gBd2wEqTn-GhtDGy4bXKrb8cOuU8TdeYjJ7rTH_NBhdhROv7TsKffqt7xqKxjyyfw*1679598466295*222862d126b2d9575e7877561a11233162fc9692c4a0b9c1152e5f726d9b5659*z16BBlre7QwBbhpHMv8OsVUOw7WyUfn8VfSb4aSvNLY"
# apiKey = "cleekks4o03790umc4rid5f9i"
headers = {"Authorization": f"Bearer {token}"}
query = """
query {
    users{
        name,
        email
    }
}
"""


# query = """
# mutation {
#   createUser(
#     data: {
#         name: "ahmed"
#         email: "ahmed@gmail.com"
#         password: "Ahmed#123#"
#     }
#   ){
#     name
#     email
#   }
# }
# """
endpoint = "https://khaled.myopenship.com/api/graphql"
r = requests.post(endpoint, json={"query": query}, headers=headers)

print(r.json())
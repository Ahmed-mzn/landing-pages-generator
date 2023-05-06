import requests


class Jonex:
    def __init__(self, customer_id, secret_key):
        self.customer_id = customer_id
        self.secret_key = secret_key

    def create(self, city, order_id):
        data = {
            "customerId": self.customer_id,
            "secret_key": self.secret_key,
            "param": {
                "BookingMode": "COD",
                "codValue": "777",
                "sender_phone": "1111111111",
                "sender_name": "Test 2 Sender",
                "sender_address": "send test 2 address",
                "description": "Test 2 shipement",
                "origin": "Riyadh",
                "receiver_phone": "222222222",
                "receiver_name": "Test2 receiver",
                "destination": city,
                "pieces": "1",
                "weight": "1",
                "receiver_address": "Test receiv address",
                "reference_id": order_id,
                "productType": "test2 parcel"
            }
        }

        res = requests.post("https://api.fastcoo-tech.com/API_v2/CreateOrder", json=data)
        print(res)
        # print(res.json())
        try:
            result = res.json()
        except:
            result = {"error": "true"}
            print("error exception")
        return result

    def tracking(self, tracking_number):
        data = {
            "awb": tracking_number
        }
        res = requests.post("https://api.fastcoo-tech.com/API/trackShipment", data=data)
        print(res)
        print(res.json())

        return res.json()

    def cancel(self, order_id):
        data = {
            "method": "cancelOrder",
            "customerId": self.customer_id,
            "param": {
                "customerId": self.customer_id,
                "booking_id": order_id
            }
        }

        res = requests.post("https://api.fastcoo-tech.com/API/deleteShipment", json=data)
        print(res)
        try:
            result = res.json()
        except:
            result = {"error": "true"}
            print("error exception")
        return result

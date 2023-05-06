import requests


class Aymakan:
    CITIES = {"Medina": {"name_ar": "Medina", "name_en": "Medine"}}

    def __init__(self, token):
        self.token = token
        self.headers = {
            'Authorization': token,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    def create(self, city):
        data = {
            "requested_by": "Test3",
            "declared_value": 111,
            "declared_value_currency": "SAR",
            "is_cod": 1,
            "cod_amount": 111,
            "currency": "SAR",
            "delivery_name": "test",
            "delivery_city": city,
            "delivery_address": "Test add",
            "delivery_neighbourhood": "Test",
            "delivery_country": "SA",
            "delivery_phone": 566932820,
            "collection_name": "test col",
            "collection_city": "Riyadh",
            "collection_address": "Test address",
            "collection_country": "SA",
            "collection_phone": 566932820,
            "weight": 12,
            "pieces": 1,
            "items_count": 1
        }

        res = requests.post("https://api.aymakan.net/v2/shipping/create", json=data, headers=self.headers)
        print(res)
        # print(res.json())

        return res.json()

    def cancel(self, tracking_number):
        data = {
            "tracking": tracking_number
        }

        res = requests.post("https://api.aymakan.net/v2/shipping/cancel", json=data, headers=self.headers)

        print(res)
        # print(res.json())
        return res.json()

    def tracking(self, tracking_number):

        res = requests.get(f"https://api.aymakan.net/v2/shipping/track/{tracking_number}", headers=self.headers)

        print(res)
        print(res.json())
        return res.json()

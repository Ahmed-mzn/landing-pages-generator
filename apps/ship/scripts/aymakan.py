import requests


class Aymakan:
    CITIES = {"Medina": {"name_ar": "Medina", "name_en": "Medine"}}

    def __init__(self, order):
        self.token = order.shipping_company.fields.filter(key='api_key').first().value
        self.order = order
        self.headers = {
            'Authorization': self.token,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    def create(self):
        data = {
            "requested_by": 'sfhat.io',
            "reference": 'SFHAT' + str(self.order.pk),
            "declared_value": str(self.order.amount),
            "declared_value_currency": "SAR",
            "is_cod": 1 if self.order.payment_type == 'cod' else 0,
            "cod_amount": 0 if self.order.payment_type != 'cod' else str(self.order.amount),
            "currency": "SAR",
            "delivery_name": self.order.lead.name,
            "delivery_city": self.order.lead.city.main_city.aymakan,
            "delivery_address": self.order.lead.address,
            "delivery_country": "SA",
            "delivery_phone": self.order.lead.phone_number,
            "collection_name": self.order.warehouse.name,
            "collection_city": self.order.warehouse.city.aymakan,
            "collection_address": self.order.warehouse.address,
            "collection_country": "SA",
            "collection_phone": self.order.warehouse.phone_number,
            "collection_email": self.order.warehouse.email,
            # "weight": 12,
            "pieces": self.order.items.count(),
            "items_count": self.order.items.count()
        }
        print(data)

        res = requests.post("https://api.aymakan.net/v2/shipping/create", json=data, headers=self.headers)
        print(res)
        print(res.text)
        try:
            print(res.json())
            if res.json()["shipping"]["tracking_number"]:
                self.order.shipping_tracking_id = res.json()["shipping"]["tracking_number"]
                self.order.shipping_awb = res.json()["shipping"]["pdf_label"]
                self.order.status = self.order.INDELIVERY
                self.order.save()
                return True
            return False
        except:
            print('error 500 aymakan')
            return False

    def cancel(self):
        data = {
            "tracking": self.order.shipping_tracking_id
        }

        res = requests.post("https://api.aymakan.net/v2/shipping/cancel", json=data, headers=self.headers)

        print(res)
        print(res.text)
        if 'success' in res.json():
            self.order.status = self.order.CANCELED
            self.order.save()
        return False

    def tracking(self):

        res = requests.get(f"https://api.aymakan.net/v2/shipping/track/{self.order.shipping_tracking_id}",
                           headers=self.headers)

        print(res)
        # print(res.json())
        tracking_info = []
        try:
            # print(res.json()["data"]["shipments"][0])
            for item in res.json()["data"]["shipments"][0]["tracking_info"]:
                tracking_info.append({
                    'code': 'cancelled' if item['status_code'] == 'AY-0029' else item['status_code'],
                    'description': item['description_ar'],
                    'created_at': item['created_at']
                })
        except:
            print('error track aymakan')
        return tracking_info

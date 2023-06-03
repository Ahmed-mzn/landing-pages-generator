import requests


class Jonex:
    def __init__(self, order):
        self.order = order
        self.customer_id = order.shipping_company.fields.filter(key='customer_id').first().value
        self.secret_key = order.shipping_company.fields.filter(key='secret_key').first().value

    def create(self):
        data = {
            "customerId": self.customer_id,
            "secret_key": self.secret_key,
            "param": {
                "BookingMode": "COD" if self.order.payment_type == 'cod' else "CC",
                "codValue": str(self.order.amount) if self.order.payment_type == 'cod' else "0",
                "sender_phone": self.order.warehouse.phone_number,
                "sender_name": self.order.warehouse.name,
                "sender_address": self.order.warehouse.address,
                "origin": self.order.warehouse.city.jonex,
                "description": ", \n".join([f"{item.product.title} x{item.quantity}" for item in self.order.items.all()]),
                "receiver_phone": self.order.lead.phone_number,
                "receiver_name": self.order.lead.name,
                "receiver_address": self.order.lead.address,
                "destination": self.order.lead.city.main_city.jonex,
                "pieces": self.order.items.count(),
                "weight": "1",
                "reference_id": 'SFHAT' + str(self.order.pk),
                "productType": "parcel"
            }
        }
        print(data)

        res = requests.post("https://api.fastcoo-tech.com/API_v2/CreateOrder", json=data)
        print(res)
        print(res.text)
        try:
            if res.json()["awb_no"]:
                self.order.shipping_tracking_id = res.json()["awb_no"]
                self.order.shipping_awb = res.json()["label_print"]
                self.order.status = self.order.INDELIVERY
                self.order.save()
                return True
            return False
        except:
            print("error create jonex")
            return False

    def tracking(self):
        data = {
            "awb": self.order.shipping_tracking_id
        }
        res = requests.post("https://api.fastcoo-tech.com/API/trackShipment", data=data)
        print(res)
        print(res.text)

        tracking_info = []

        try:
            for item in res.json()['travel_history']:
                tracking_info.append({
                    'code': 'cancelled' if item['Activites'] == 'Order Deleted' else item['Activites'],
                    'description': item['new_status_ar'],
                    'created_at': item['entry_date']
                })
        except:
            print('error track jonex')
        return tracking_info

    def cancel(self):
        data = {
            "method": "cancelOrder",
            "customerId": self.customer_id,
            "param": {
                "customerId": self.customer_id,
                "booking_id": 'SFHAT' + str(self.order.pk)
            }
        }

        res = requests.post("https://api.fastcoo-tech.com/API/deleteShipment", json=data)
        print(res)
        print(res.text)
        try:
            result = res.json()
            self.order.status = self.order.CANCELED
            self.order.save()
        except:
            result = {"error": "true"}
            print("error exception")
        return result

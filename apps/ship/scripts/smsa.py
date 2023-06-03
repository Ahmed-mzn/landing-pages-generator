import requests
import datetime
import json
import zeep
import base64


class Smsa:
    def __init__(self, order):
        self.order = order
        self.pass_key = order.shipping_company.fields.filter(key='pass_key').first().value
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    def create(self):
        params = {
            "passkey": self.pass_key,
            "refno": 'SFHAT' + str(self.order.pk),
            "sentDate": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "idNo": 'SFHAT' + str(self.order.pk),
            "cName": self.order.lead.name,
            "cntry": "KSA",
            "cCity": self.order.lead.city.main_city.smsa,
            "cZip": "",
            "cPOBox": "",
            "cMobile": self.order.lead.phone_number,
            "cTel1": "",
            "cTel2": "",
            "cAddr1": self.order.lead.address,
            "cAddr2": "",
            "shipType": "DLV",
            "PCs": 1,
            "cEmail": "",
            "carrValue": "",
            "carrCurr": "SAR",
            "codAmt": str(self.order.amount) if self.order.payment_type == 'cod' else "0",
            "weight": 1.0,
            "itemDesc": ", \n".join([f"{item.product.title} x{item.quantity}" for item in self.order.items.all()]),
            "custVal": "",
            "custCurr": "",
            "insrAmt": "",
            "insrCurr": "",
            "sName": self.order.warehouse.name,
            "sContact": self.order.warehouse.name,
            "sAddr1": self.order.warehouse.address,
            "sAddr2": "",
            "sCity": self.order.warehouse.city.smsa,
            "sPhone": self.order.warehouse.phone_number,
            "sCntry": "KSA",
            "prefDelvDate": "",
            "gpsPoints": ""
        }

        res = requests.post(f"https://track.smsaexpress.com/SecomRestWebApi/api/addship?api_key={self.pass_key}",
                            data=json.dumps(params), headers=self.headers)
        print(res.text)
        try:
            if res.json():
                self.order.shipping_tracking_id = res.json()
                self.order.status = self.order.INDELIVERY
                self.order.save()
                return True
        except:
            print("error create jonex")
            return False
        return False

    def tracking(self):
        res = requests.get(f"https://track.smsaexpress.com/SecomRestWebApi/api/getTracking?passKey={self.pass_key}&awbno={self.order.shipping_tracking_id}&api_key={self.pass_key}")
        print(res.text)
        tracking_info = []
        try:
            for item in res.json()['Tracking']:
                tracking_info.append({
                    'code': 'cancelled' if item['Activity'] == 'CANCELLED ON CLIENTS REQUEST' else ['Activity'],
                    'description': item['Details'],
                    'created_at': item['Date']
                })
        except:
            print('error track smsa')
        return tracking_info

    def cancel(self):
        wsdl = 'https://track.smsaexpress.com/SECOM/SMSAwebService.asmx?wsdl'
        client = zeep.Client(wsdl=wsdl)

        response = client.service.cancelShipment(self.order.shipping_tracking_id, self.pass_key, 'Online Ship Canceled')
        print(response)
        if 'Failed' not in response:
            self.order.status = self.order.CANCELED
            self.order.save()
        return True

    def get_awb(self):
        res = requests.get(f"https://track.smsaexpress.com/SecomRestWebApi/api/getPDF?passKey={self.pass_key}&awbno={self.order.shipping_tracking_id}&api_key={self.pass_key}")
        return res.content

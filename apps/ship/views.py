from django.shortcuts import render

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .models import Channel, ConstantChannel, Order, OrderItem, Coupon, Warehouse
from .serializers import ChannelSerializer, ConstantChannelSerializer, OrderItemSerializer, OrderSerializer, \
    CouponSerializer, AffiliateSerializer, WarehouseSerializer


from .scripts.aymakan import Aymakan
from .scripts.jonex import Jonex

from apps.main.helpers import best
from apps.main.models import Affiliate

import requests
import json
import os
import uuid
import datetime


class ChannelAPI(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return self.queryset.filter(app__user=self.request.user)


class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return self.queryset.filter(app__user=self.request.user)


class AffiliateViewSet(viewsets.ModelViewSet):
    queryset = Affiliate.objects.all()
    serializer_class = AffiliateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return self.queryset.filter(app__user=self.request.user)


class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return self.queryset.filter(app__user=self.request.user)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        if self.request.GET.get('template_id', ''):
            template_id = self.request.GET.get('template_id', '')
            return self.queryset.filter(template__app__user=self.request.user, template_id=template_id)
        return self.queryset.filter(template__app__user=self.request.user)

    @action(methods=["POST"], detail=False, url_path="public", authentication_classes=[], permission_classes=[])
    def create_public(self, request):
        data = self.request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_constant_channels(request):
    channels = ConstantChannel.objects.all()
    serializer = ConstantChannelSerializer(instance=channels, many=True)

    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def test(request):

    customer_id = "100358618"
    secret_key = "ee2aaa-5bad15-fb2b89-ab569c-0faad4"
    result = Jonex(customer_id, secret_key).cancel('SFH987654321')
    # return Response(data={'msg': 'ok', 'res': result})

    # all_data = []
    #
    # token = "05810ffa6b23cad68e7ffc95b17d40283e7b629c891491d39035b97ebe5a9f5e3f9f305914"
    # headers = {
    #     "Authorization": f"Bearer {token}"
    # }
    # for i in range(1, 60):
    #     print(i)
    #     res = requests.get(f"https://api.salla.dev/admin/v2/countries/1473353380/cities?page={i}", headers=headers)
    #     print(res)
    #     data = res.json()['data']
    #     all_data += data
    all_data = best()
    new_data = []
    module_dir = os.path.dirname(__file__)

    token = "7e3347c7a4fa5373af1d2887221ba0ea-def760d1-7321-41a7-bd18-348c6c0d5096-759fa5d9ea6084c17f879a91fa9ec563/4d1b293846bb1fe5b1a31b5843b43cfe/b186b6ba-1dd9-4b32-a5ed-84669f1381ee"
    f_test = open(os.path.join(module_dir, "salla.json"), encoding='utf-8')
    data_test = json.load(f_test)
    indice = 0

    # Creat test aymakan
    # for item in data_test:
    #     indice += 1
    #     print(item["name"])
    #     print(indice)
    #     result = Aymakan(token).create(item["name"])
    #     result["id"] = item["id"]
    #     result["name"] = item["name"]
    #     result["name_en"] = item["name_en"]
    #     new_data.append(result)

    # delete Test aymakan
    # for item in data_test:
    #     if "success" in item:
    #         print(item["shipping"]["tracking_number"])
    #         result = Aymakan(token).cancel(item["shipping"]["tracking_number"])
    #         indice += 1
    #         print(indice)
    #         new_data.append(result)

    # Create Test JONEX
    # for item in data_test:
    #     indice += 1
    #     order_id = str(uuid.uuid4())
    #     print(item["name"])
    #     print(str(indice) + " ---> " + order_id)
    #     result = Jonex(customer_id, secret_key).create(item["name_en"], order_id)
    #     result["id"] = item["id"]
    #     result["name"] = item["name"]
    #     result["name_en"] = item["name_en"]
    #     new_data.append(result)

    # delete jonex test
    # for item in data_test:
    #     if "order_id" in item:
    #         print(item["order_id"])
    #         result = Jonex(customer_id, secret_key).cancel(item["order_id"])
    #         indice += 1
    #         print(indice)
    #         new_data.append(result)

    # f_salla = open(os.path.join(module_dir, "salla.json"), encoding='utf-8')
    # data_salla = json.load(f_salla)
    # indice = 0
    # for item in data_salla:
    #     indice += 1
    #     result = Aymakan(token).create(item["name"])
    #     print(item["name"])
    #     new_data.append(result)
    # for item in all_data:
    #     if item["aymakan_ar"] != "" or item["aymakan_en"] != "":
    #         new_data.append(item)

    # aramex test
    data = {
        "ClientInfo": {
            "UserName": "testingapi@aramex.com",
            "Password": "R123456789$r",
            "Version": "v1",
            "AccountNumber": "20016",
            "AccountPin": "331421",
            "AccountEntity": "AMM",
            "AccountCountryCode": "JO",

        },
        "LabelInfo": None,
        "Shipments": [
            {
                "Reference1": "",
                "Reference2": "",
                "Reference3": "",
                "Shipper": {  # shipper details
                    "Reference1": "",
                    "Reference2": "",
                    "AccountNumber": "20016",  # required
                    "PartyAddress": {
                        "Line1": "Test address",  # required
                        "Line2": "",
                        "Line3": "",
                        "City": "amman",  # required
                        "StateOrProvinceCode": "",
                        "PostCode": "",
                        "CountryCode": "JO",  # required
                        "Longitude": 0,  # required
                        "Latitude": 0,  # required
                        "BuildingNumber": None,
                        "BuildingName": None,
                        "Floor": None,
                        "Apartment": None,
                        "POBox": None,
                        "Description": None
                    },
                    "Contact": {
                        "Department": None,
                        "PersonName": "Test",
                        "Title": None,
                        "CompanyName": "Test Fafwat",
                        "PhoneNumber1": "966566932820",
                        "PhoneNumber1Ext": None,
                        "PhoneNumber2": None,
                        "PhoneNumber2Ext": None,
                        "FaxNumber": None,
                        "CellPhone": "966566932820",
                        "EmailAddress": "test@test.com",
                        "Type": None,
                    }
                },
                "Consignee": {  # customer Details
                    "Reference1": "",
                    "Reference2": "",
                    "AccountNumber": "20016",
                    "PartyAddress": {
                        "Line1": "Test customer address",  # required
                        "Line2": "",
                        "Line3": "",
                        "City": "aman",  # required
                        "StateOrProvinceCode": "",
                        "PostCode": "",
                        "CountryCode": "JO",
                        # required
                        "Longitude": 0,  # required
                        "Latitude": 0,  # required
                        "BuildingNumber": None,
                        "BuildingName": None,
                        "Floor": None,
                        "Apartment": None,
                        "POBox": None,
                        "Description": None
                    },
                    "Contact": {
                        "Department": None,
                        "PersonName": "customer.name",
                        "Title": None,
                        "CompanyName": "customer.name",
                        "PhoneNumber1": "962799999999",
                        "PhoneNumber1Ext": None,
                        "PhoneNumber2": None,
                        "PhoneNumber2Ext": None,
                        "FaxNumber": None,
                        "CellPhone": "962799999999",
                        "EmailAddress": "cus@test.com",
                        "Type": None,
                    }
                },
                "ShippingDateTime": r"\/Date(%s000-0500)\/" % int(datetime.datetime.timestamp(datetime.datetime.now())), # required
                "DueDate": r"\/Date(%s000-0500)\/" % int(datetime.datetime.timestamp(datetime.datetime.now())), # required
                "Comments": "",
                "PickupLocation": "",
                "OperationsInstructions": "",
                "AccountingInstrcutions": "",
                "Details": {
                    "Dimensions": None,
                    "ActualWeight": {
                        "Unit": "KG",  # required
                        "Value": 0.5  # required
                    },
                    "ChargeableWeight": None,
                    "DescriptionOfGoods": "nature content",  # required
                    "GoodsOriginCountry": "SA",  # required
                    "NumberOfPieces": 12,  # required
                    "ProductGroup": "DOM",  # "DOM", # required| International EXP
                    "ProductType": "CDS",  # "CDS", # required | International EPX
                    "PaymentType": "P",
                    # 'P' , # required | International 3 - meaning if the shipment origin is not riyadh
                    "PaymentOptions": "",
                    "CashOnDeliveryAmount": {
                        'CurrencyCode': "SAR",
                        'Value': 100
                    },
                    "InsuranceAmount": None,
                    "CashAdditionalAmount": None,
                    "CashAdditionalAmountDescription": "",
                    "CollectAmount": None,
                    "CustomsValueAmount": None,
                    "Services": "",
                    "Items": []
                },
                "Attachments": [],
                "ForeignHAWB": "Ref12345",
                "TransportType ": 0,
                "PickupGUID": "",
                "Number": None,
                "ScheduledDelivery": None
            }
        ],
        "Transaction": {
            "Reference1": "",
            "Reference2": "",
            "Reference3": "",
            "Reference4": "",
            "Reference5": ""
        }
    }

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    # params = json.dumps(data, indent=2)
    # res = requests.post("https://ws.dev.aramex.net/ShippingAPI.V2/Shipping/Service_1_0.svc/json/CreateShipments", data=params.replace("\\\\", "\\"), headers=headers)
    # print(res.text)

    # aramex ship status tracking
    params = {
        "ClientInfo": {
            "UserName": "testingapi@aramex.com",
            "Password": "R123456789$r",
            "Version": "v1",
            "AccountNumber": "20016",
            "AccountPin": "331421",
            "AccountEntity": "AMM",
            "AccountCountryCode": "JO",

        },
        "GetLastTrackingUpdateOnly": False,
        "Shipments": [
            "44164123802"
        ],
        "Transaction": {
            "Reference1": "",
            "Reference2": "",
            "Reference3": "",
            "Reference4": "",
            "Reference5": "",
        }
    }

    # res = requests.post("https://ws.dev.aramex.net/ShippingAPI.V2/Tracking/Service_1_0.svc/json/TrackShipments", data=json.dumps(params), headers=headers)
    # print(res.text)

    # get label
    params = {
        "ClientInfo": {
            "UserName": "testingapi@aramex.com",
            "Password": "R123456789$r",
            "Version": "v1",
            "AccountNumber": "20016",
            "AccountPin": "331421",
            "AccountEntity": "AMM",
            "AccountCountryCode": "JO",

        },
        "LabelInfo": {
            "ReportID": 9729,
            "ReportType": "URL",
        },
        "OriginEntity": "",
        "ProductGroup": "EXP",
        "ShipmentNumber": "44164123802",
        "Transaction": {
            "Reference1": "",
            "Reference2": "",
            "Reference3": "",
            "Reference4": "",
            "Reference5": "",
        }
    }

    # res = requests.post("https://ws.dev.aramex.net/ShippingAPI.V2/Shipping/Service_1_0.svc/json/PrintLabel", data=json.dumps(params), headers=headers)
    # print(res.json())

    # smsa express test
    for item in data_test:
        indice += 1
        print(indice)
        order_id = str(uuid.uuid4())
        params = {
            "passkey": "Testing2",
            "refno": order_id,
            "sentDate": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "idNo": "ownerRef1234",
            "cName": "customer name",
            "cntry": "KSA",
            "cCity": item["name"],
            "cZip": "",
            "cPOBox": "",
            "cMobile": "966566932820",
            "cTel1": "",
            "cTel2": "",
            "cAddr1": "test add one",
            "cAddr2": "",
            "shipType": "DLV",
            "PCs": 1,
            "cEmail": "test@test.com",
            "carrValue": "",
            "carrCurr": "SAR",
            "codAmt": 123,
            "weight": 1.0,
            "itemDesc": "item, desc",
            "custVal": "",
            "custCurr": "",
            "insrAmt": "",
            "insrCurr": "",
            "sName": "own name",
            "sContact": "shipment.owner_id.name",
            "sAddr1": "shipment.owner_id.add",
            "sAddr2": "",
            "sCity": "Riyadh",
            "sPhone": "966566932820",
            "sCntry": "KSA",
            "prefDelvDate": "",
            "gpsPoints": ""
        }

        res = requests.post("https://track.smsaexpress.com/SecomRestWebApi/api/addship?api_key=Testing2", data=json.dumps(params), headers=headers)
        print(res.text)
        new_data.append(res.text)

    # get status
    # res = requests.get("https://track.smsaexpress.com/SecomRestWebApi/api/getTracking?passKey=Testing2&awbno=290430865886&api_key=Testing2")
    # print(res.json())

    # get label awb
    # res = requests.get("https://track.smsaexpress.com/SecomRestWebApi/api/getPDF?passKey=Testing2&awbno=290430865886&api_key=Testing2")
    # print(res.json())

    return Response(data={'msg': 'ok', 'res': new_data})

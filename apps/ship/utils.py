import os
import time
import requests

from .models import Channel, Warehouse

from .scripts.aymakan import Aymakan
from .scripts.jonex import Jonex
from .scripts.smsa import Smsa
import threading


def create_ship(order):
    app = order.template.app
    warehouse = Warehouse.objects.filter(app=app, is_current=True).first()
    channels = [channel.id for channel in app.channels.filter(is_active=True).order_by("id")]
    channels_count = app.channels.count()
    is_shipped = False
    channel = None
    if channels_count != 0:
        print('[+] start ship creation')
        next_ship_channel = app.next_ship_channel

        if next_ship_channel == 0:
            channel = Channel.objects.get(pk=channels[0])
        else:
            try:
                channel = Channel.objects.get(pk=next_ship_channel)
            except:
                channel = Channel.objects.get(pk=channels[0])
        current_channel_index = channels.index(channel.id)
        # print(channels)
        # print(current_channel_index)
        order.shipping_company = channel
        order.warehouse = warehouse
        order.save()

        if channel.type == 'aymakan':
            is_shipped = Aymakan(order).create()

        if channel.type == 'jonex':
            is_shipped = Jonex(order).create()

        if channel.type == 'smsa':
            is_shipped = Smsa(order).create()

        if is_shipped:
            if current_channel_index == (channels_count-1):
                app.next_ship_channel = channels[0]
            else:
                app.next_ship_channel = channels[current_channel_index+1]
            app.save()

        headers = {
            'Authorization': 'Bearer EAAC4eE8WAOkBO1NjrlEWyaHhRUrj5uyZBx5a2asZCQKo9ht8EeksJhvzmKi2MYaohIgIXMjaODijpvT6iiphXo1ZCL6NNhLDakfmwZC4vEGxZBZC68sF5VNS0xQgJPcWdYEh4AyADWsVwkClNsiaunzDRUBCJX0q43TJcy72ik8ZBIAV8ZA5kdUB9Em3AqdnyKsw81fltinyNeYMzH8Q'
        }
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": "22220004200",
            "type": "template",
            "template": {
                "name": "indelivery_1688226612",
                "language": {
                    "code": "ar"
                },
                "components": [
                    {
                        "type": "header",
                        "parameters": [
                            {
                                "type": "image",
                                "image": {
                                    "link": "https://b.top4top.io/p_2738i6gqn1.jpg"
                                }
                            }
                        ]
                    },
                    {
                        "type": "body",
                        "parameters": [
                            {
                                "type": "text",
                                "text": order.lead.name
                            },
                            {
                                "type": "text",
                                "text": "https://aymakan.com.sa/en/tracking/173926"
                            }
                        ]
                    }
                ]
            }
        }
        res = requests.post("https://graph.facebook.com/v14.0/109351868894671/messages", headers=headers, json=data)
        print(res)
        print(res.text)

        print('[+] Finish ship creation')
        return is_shipped
    return is_shipped


def delete_temps(files):
    print('[+] Start process delete files')
    time.sleep(5)
    for file in files:
        try:
            os.remove(file.name)
        except:
            print('erros')
    print('[+] Finish process delete files')
    return True

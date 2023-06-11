from notifiers import get_notifier
import time

import requests
apiToken = '6170324561:AAHVgbJgYR3nn15K28nFqGHN-xlEtI7yhFM'
chatID = '527189256'

def notify(order):
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': order})
        print(response.text)
    except Exception as e:
        print(e)

notify('new_order_incoming')

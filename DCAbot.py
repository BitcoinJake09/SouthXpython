#!/usr/bin/env python3
import ssl
import websocket
import requests
import decimal
import json
from config import *
import time
import urllib.parse
import hashlib
import hmac

currencyToBuy = 'DVT'
currencyToTrade = 'BTC'
amountToBuy = '2'
#time in seconds is how often you want to buy the asset
timeInMinutes = 1;


starttime = time.time()
while True:
    URL = "https://www.southxchange.com/api/price/DVT/BTC"
    PARAMS = {}
    r = requests.get(url = URL, params = PARAMS)
    data = r.json()
    print ("result '%s'" % data)
    bid = data["Bid"]
    ask = data["Ask"]
    last = data["Last"]
    #print ("Bid: " + str(bid))
    print ("Ask: " + str(ask))
    #print ("Last: " + str(last))
    timeInMilliseconds = int(round(time.time() * 1000))
    json_data = {"nonce": timeInMilliseconds, "key": API_Key, "listingCurrency": currencyToBuy,"referenceCurrency": currencyToTrade,"type":"buy", "amount": amountToBuy, "limitPrice":str(ask)}
    hash = hmac.new(Secret_Key, json.dumps(json_data).encode('utf8'), hashlib.sha512).hexdigest()
    headers = {
    'Hash': hash,
    'Content-Type': 'application/json'
    }
    print ("bought: " + str(amountToBuy) + " " + currencyToBuy + " at "+ str(ask) + " each.")
    url = "https://www.southxchange.com/api/listBalances"
    response = requests.post(url = "https://www.southxchange.com/api/placeOrder", json = json_data, headers = headers)
    result = json.loads(response.text)
    print ("result: " + str(result))
    timeInMilliseconds = int(round(time.time() * 1000))
    json_data = {"nonce": timeInMilliseconds, "key": API_Key}
    hash = hmac.new(Secret_Key, json.dumps(json_data).encode('utf8'), hashlib.sha512).hexdigest()
    headers = {
    'Hash': hash,
    'Content-Type': 'application/json'
    }
    url = "https://www.southxchange.com/api/listBalances"
    response = requests.post(url = url, json = json_data, headers = headers)
    result = json.loads(response.text)
    for balance in result:
     print(balance["Currency"] + ": " + str(balance["Available"]))
    time.sleep((60.0 * timeInMinutes) - ((time.time() - starttime) % (60.0 * timeInMinutes)))

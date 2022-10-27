import logging
import pprint
import time
import requests

def init():
    logging.basicConfig(filename='PriceDrop.log', encoding='utf-8', level=logging.INFO,
                        format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')

def postMessageToDiscord(message):
    # Webhook URL
    discordUrl = 'https://discordapp.com/api/webhooks/1035155414653878272/6m_Mvf516qLbxA9RGHRRJRzq1RE3TgWORQQ3pXdyHLD3dd_m56LEZEAkj-P04B4LaB5l'

    data = {
        "content": message,
        "username": "Price Drop"
    }

    result = requests.post(discordUrl, json=data)

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Payload delivered successfully, code {}.".format(result.status_code))

def get_wegld_price():
    url = 'https://microservice.jexchange.io/prices/WEGLD-bd4d79'
    response = requests.get(url)
    response.raise_for_status()  # raise exception if invalid response
    jsondata = response.json()
    return jsondata["rate"]

def get_allOffers(wegld_price, price_limit_to_notify):
    url = 'https://microservice.jexchange.io/v3/offers?token_a_identifier=ASH-a642d1&token_b_identifier=WEGLD-bd4d79&status=0&hide_reserved_offers=true&skip=0&limit=9'
    response = requests.get(url)
    response.raise_for_status() # raise exception if invalid response
    jsondata = response.json()
    #pprint.pprint(jsondata) # prettyprint the json

    # Get Token String
    separator = '-'
    token_to_buy = jsondata[0]["token_a_identifier"].split(separator, 1)[0]

    cheapest_price = round(jsondata[0]["rate"]*wegld_price, 4)
    # Also check second cheapest price for more reliability
    second_cheapest_price = round(jsondata[1]["rate"]*wegld_price, 4)

    # Always print & log cheapest price
    print(f'Current Price for 1 {token_to_buy}: {cheapest_price} $ ')
    logging.info(f'Cheapest Price: {cheapest_price} $')
    logging.info(f'Second cheapest Price: {second_cheapest_price} $')

    if(cheapest_price < price_limit_to_notify):
        message = f'{token_to_buy} (< {price_limit_to_notify} $) = {cheapest_price} $'
        postMessageToDiscord(message)
    elif(second_cheapest_price < price_limit_to_notify):
        message = f'{token_to_buy} (< {price_limit_to_notify} $) = {second_cheapest_price} $'
        postMessageToDiscord(message)

if __name__ == '__main__':
    init()
    #price_limit_to_notify = float(input("Preisgrenze ab wann gelogged wird: "))
    price_limit_to_notify = 0.10
    sleeptime = 10
    while True:
        print('')
        print('----------START----------')
        wegld_price = get_wegld_price()
        print(f'1 WEGLD = {round(wegld_price, 2)} $')
        get_allOffers(wegld_price, price_limit_to_notify)
        print('----------END----------')
        for x in range(sleeptime):
            #if (x%2 == 0):
                #print(f'--- {sleeptime-x} Sec Waiting... ---')
            time.sleep(1)
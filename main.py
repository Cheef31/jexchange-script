import logging
import pprint
import time
import requests

def init():
    logging.basicConfig(filename='PriceDrop.log', encoding='utf-8', level=logging.INFO,
                        format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')

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
    #pprint.pprint(jsondata)

    # Get Token String
    separator = '-'
    token_to_buy = jsondata[0]["token_a_identifier"].split(separator, 1)[0]
    token_to_buy_with = jsondata[0]["token_b_identifier"].split(separator, 1)[0]

    # Always log cheapest price
    logging.info(f'Cheapest Price: {round(jsondata[0]["rate"]*wegld_price, 4)} $')

    # Print
    print('Prices for 1 ' + token_to_buy + ' in ' + token_to_buy_with + ' on JEXchange.io')
    print('----------------------------------------')
    for x in jsondata:
        r = x["rate"]
        r_USD = r * wegld_price
        print(f'{round(r_USD, 4)} $')

        if(r_USD < price_limit_to_notify):
            print('LOG PRICE DROP')
            logging.info(f'PRICE DROP under {price_limit_to_notify} $ to: {r_USD} $')

if __name__ == '__main__':
    init()
    # price_limit_to_notify = float(input("Preisgrenze ab wann gelogged wird: "))
    price_limit_to_notify = 0.07
    sleeptime = 10
    while True:
        print('')
        wegld_price = get_wegld_price()
        print(f'1 WEGLD = {round(wegld_price, 2)} $')
        print('----------START----------')
        get_allOffers(wegld_price, price_limit_to_notify)
        print('----------END----------')
        for x in range(sleeptime):
            #if (x%2 == 0):
                #print(f'--- {sleeptime-x} Sec Waiting... ---')
            time.sleep(1)
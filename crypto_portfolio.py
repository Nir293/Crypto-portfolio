from binance.client import Client
import pandas as pd
api_key = 'api_key'
api_secret='api_secret'
client = Client(api_key, api_secret)
base_path = 'https://api.binance.com'

my_pairs = ['BTCUSDT', 'BTCBUSD', 'BTCUPUSDT',
            'BTCDOWNUSDT', 'FIOUSDT', 'FIOBUSD',
            'BNBBUSD', 'BNBUSDT', 'BNBDOWNUSDT', 
            'BNBBTC', 'XRPDOWNUSDT', 'ETHUSDT',
            'FILDOWNUSDT', 'ETHBTC', 'FIOUSDT',
            'ADAUSDT', 'DOGEBUSD', 'FIOBUSD',
            'DOTUSDT', 'ETHUPUSDT', 'SHIBUSDT',
            'QTUMUSDT', 'LINKUSDT', 'MANAUSDT',
            'RENUSDT', 'MATICUSDT', 'ICPUSDT',
            'LINKUSDT', 'MDXUSDT', 'LTCUSDT',
            'ADAUPUSDT','FIOBTC','DOGEUSDT',
            'SCUSDT','OMGUSDT','IOSTUSDT',
            'OMGBTC','MATICBTC','THETAUSDT',
            'ADABTC','MANABTC','HBARUSDT',
            'XMRUSDT','XRPUSDT','ONEUSDT',
            'ETHDOWNUSDT','WINUSDT','IOSTBTC',
            'SCBTC','DOGEBTC','RENBTC',
            'DOTBTC','DOTBUSD','XMRBTC',
            'LUNABTC']

# extracting the signle symbols for the dataframe index
info = client.get_exchange_info()
better_info = []
my_symbols = []
for t in my_pairs:
    for z in range(len(info['symbols'])):
        if t == info['symbols'][z]['symbol']:
            better_info.append(info['symbols'][z]['baseAsset'])
            better_info.append(info['symbols'][z]['quoteAsset'])
for v in better_info:
    if v not in my_symbols:
        my_symbols.append(v)
    
# get my orders and filter the filled ones
my_orders = []
my_filled_orders = []
for i in my_pairs:
    my_orders.append(client.get_all_orders(symbol=i, limit=500))   
for x in range(len(my_orders)):
    for y in range(len(my_orders[x])):
        if my_orders[x][y]['status'] == 'FILLED':
            my_filled_orders.append(my_orders[x][y])

# cleaning duplicate orders
my_clean_orders = []
for t in my_filled_orders:
    if t not in my_clean_orders:
        my_clean_orders.append(t)

# Generating my balance and inculing current price and value in dollars
my_balance = pd.DataFrame(None,columns=['Total','Current price'], index =(my_symbols) )
my_balance.loc[:,'Total'] = 0
my_balance.loc[:,'Current price'] = 0
my_balance.loc[:,'Value in USD'] = 0
def balance_generator():
    id_list = []   
    for idx,x in enumerate(my_clean_orders):
        for coin1 in my_symbols:
            if my_clean_orders[idx]['symbol'].startswith(coin1) and my_clean_orders[idx]['symbol'].replace(coin1,'') in my_symbols and my_clean_orders[idx]['orderId'] not in id_list:
                coin2 = my_clean_orders[idx]['symbol'].replace(coin1,'')
                if my_clean_orders[idx]['side'] == 'BUY' and my_clean_orders[idx]['clientOrderId'] not in id_list:
                    id_list.append(my_clean_orders[idx]['orderId'])
                    my_balance.loc[coin1,'Total'] += float(my_clean_orders[idx]['executedQty'])
                    my_balance.loc[coin2,'Total'] -= float(my_clean_orders[idx]['cummulativeQuoteQty'])
                elif my_clean_orders[idx]['side'] == 'SELL' and my_clean_orders[idx]['clientOrderId'] not in id_list:
                    id_list.append(my_clean_orders[idx]['orderId'])
                    my_balance.loc[coin1,'Total'] -= float(my_clean_orders[idx]['executedQty'])
                    my_balance.loc[coin2,'Total'] += float(my_clean_orders[idx]['cummulativeQuoteQty'])
    prices = client.get_all_tickers()
    usd_prices = []
    for symbol in my_symbols:
        for i in range(len(prices)):
            if symbol + 'USDT' == prices[i]['symbol']:
                usd_prices.append(prices[i])
    for t in my_balance.index:
        for z in range(len(usd_prices)):
            if usd_prices[z]['symbol'] == t + 'USDT':
                my_balance.loc[t,'Current price'] = usd_prices[z]['price']
            elif t =='USDT' or t == 'BUSD':
                my_balance.loc[t,'Current price'] = 1
                
    for m in my_balance.index:
        my_balance.loc[m,'Value in USD'] = float(my_balance.loc[m,'Total'])*float(my_balance.loc[m,'Current price'])
    for j in my_balance.index:
        if j == 'USDT' or j == 'BUSD':
            continue
        elif my_balance.loc[j,'Value in USD']<= 0:
            my_balance.loc[j,'Value in USD'] = 0                 

balance_generator()                

    
    
from pandas_datareader import data as pdr
import yfinance as yf

yf.pdr_override() # <== that's all it takes :-)

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Configs
today = datetime.today()
if today.weekday() >= 5 :
    last_weekday = today - timedelta(days=(today.weekday() + 2) % 6)
    start_day = last_weekday
else:
    start_day = today


common_stock_symbols = [
    'ASIANPAINT',
    'AXISBANK',
    'BAJAJ-AUTO',
    'BAJAJFINSV',
    'BAJFINANCE',
    'BHARTIARTL',
    'BPCL',
    'CIPLA',
    'COALINDIA',
    'DRREDDY',
    'EICHERMOT',
    'GAIL',
    'GRASIM',
    'HCLTECH',
    'HDFC',
    'HDFCBANK',
    'HEROMOTOCO',
    'HINDALCO',
    'HINDPETRO',
    'HINDUNILVR',
    'ICICIBANK',
    'INDUSINDBK',
    'INFY',
    'IOC',
    'ITC',
    'JSWSTEEL',
    'KOTAKBANK',
    'LT',
    'M&M',
    'MARUTI',
    'NESTLEIND',
    'NTPC',
    'ONGC',
    'POWERGRID',
    'RELIANCE',
    'SBIN',
    'SHREECEM',
    'SUNPHARMA',
    'TATAMOTORS',
    'TATASTEEL',
    'TCS',
    'TECHM',
    'TITAN',
    'UPL',
    'ULTRACEMCO',
    'WIPRO'
]

def get_opportunities():
    
    # get stock data
    stock_data = []
    
    for ticker in common_stock_symbols:
        # Tickers
        tickers_ns = ticker + ".NS"
        tickers_bo = ticker + ".BO"

        # Data
        ns_pr = pdr.get_data_yahoo(tickers_ns, start=start_day)
        bo_pr = pdr.get_data_yahoo(tickers_bo, start=start_day)

        if len(ns_pr) > 0 and len(bo_pr) > 0:
            ns_data = {'NS_' + k: p for k, p in [v for v in ns_pr.to_dict(orient='index').values()][0].items()}
            bo_data = {'BO_' + k: p for k, p in [v for v in bo_pr.to_dict(orient='index').values()][0].items()}

            temp = {
                'stock': ticker
            }

            temp.update(ns_data)
            temp.update(bo_data)
            
            stock_data.append(temp)

    # Calculating Opportunity
        df = pd.DataFrame(stock_data)
        df['Opportunity'] = np.abs(df['NS_Close'] - df['BO_Close']) 
        df['Opportunity%'] = df['Opportunity'] / df['BO_Close'] * 100
        df.sort_values(by='Opportunity%', ascending=False, inplace=True)

        df.to_csv('../data/processed/{}.csv'.format(start_day), index=False)


if __name__ == '__main__':
    get_opportunities()
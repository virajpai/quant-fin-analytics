import requests
from bs4 import BeautifulSoup

import pandas as pd

from time import sleep

import streamlit as st

def get_qvt(ticker: str) -> dict:

    # Get QVT URL and source
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    url = f'https://trendlyne.com/web-widget/qvt-widget/Poppins/{ticker}'
    response = requests.get(url, headers=headers)

    if response.status_code == 403:
        sleep(60) # Wait 1 minute
        response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.content, 'html.parser')

    # Get the only div tag
    div = soup.find('div')

    # Parse all required attributes
    stock = div.get_attribute_list('data-stock-name')[0]
    qvt = dict(eval(div.get_attribute_list('data-qvt-result')[0].replace("null", "None")))

    q = qvt.get('quality').get('value')
    qi = qvt.get('quality').get('insight')

    v = qvt.get('valuation').get('value')
    vi = qvt.get('valuation').get('insight')

    t = qvt.get('technical').get('value')
    ti = qvt.get('technical').get('insight')

    st = qvt.get('st')
    lt = qvt.get('lt')

    tmp = {
        'Ticker': ticker,
        'Stock Name': stock,
        'Quality': int(round(q, 0)) if q is not None else None,
        'Quality Insight': qi,
        'Valuation': int(round(v, 0)) if v is not None else None,
        'Valuation Insight': vi,
        'Technical': int(round(t, 0)) if t is not None else None,
        'Technical Insight': ti,
        'Comment1': st,
        'Comment2': lt 
    }

    return tmp


# URL to get the list of NSE stocks
nse_tickers_url = '../data/static/ind_nifty500list.csv'

# Read the data from the URL
tickers_df = pd.read_csv(nse_tickers_url)

# Extract the Symbol column
tickers = tickers_df['Symbol'].tolist()

# Print all NSE tickers
qvt_df = []
for ticker in tickers:
    print(ticker)
    qvt_df.append(get_qvt(ticker))
    sleep(10)

df = pd.DataFrame(qvt_df).sort_values('Valuation', ascending=False)
df['Avg QVT'] = (df['Quality'].fillna(0) + df['Valuation'].fillna(0) + df['Technical'].fillna(0)) / 3
# df.sort_values(['Avg QVT', 'Valuation'], ascending=[False, False])

st.dataframe(df)
# st.dataframe(df.style.highlight_max(axis=0))

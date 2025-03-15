import yfinance as yf

from datetime import datetime

import pandas as pd
import numpy as np

from matplotlib import pyplot as plt
from matplotlib import cm


import seaborn as sns

def get_historic_df(stock_tickers, period=3*365):
    """
    Fetches historical closing prices of given stock tickers for the last 'period' days.
    
    Parameters:
        stock_tickers (list): List of stock ticker symbols.
        period (int): Number of days of historical data to fetch (default: 3 years).
    
    Returns:
        pd.DataFrame: DataFrame with date as index and stock tickers as columns.
    """
    # Calculate start date based on the given period
    start_date = pd.Timestamp.today() - pd.Timedelta(days=period)
    
    # Download data from Yahoo Finance
    df = yf.download(stock_tickers, start=start_date.strftime('%Y-%m-%d'))["Close"]
    
    return df

def simulate_portfolio(stocks, stock_qty, hist_years=3, T=4*3, dt=30*3, n_sim=10000):
    
    # Get historic data
    df = get_historic_df(stocks, period=365*hist_years)[stocks]

    # Compute log returns = ln(previous day/current day)
    log_returns = np.log(df / df.shift(1)).dropna()

    # Compute statistics
    mu = log_returns.mean()
    sigma = log_returns.std()
    correlation_matrix = log_returns.corr()

    # Monte Carlo simulation
    S0 = df.iloc[-1].values  # Last known prices
    L = np.linalg.cholesky(correlation_matrix.values)  # Cholesky decomposition for correlation

    # Number of stocks in portfolio
    num_stocks = len(df.columns)

    # Initialize paths
    paths = np.zeros((T, num_stocks, n_sim))
    paths[0, :, :] = S0.reshape(-1, 1)

    # Simulate correlated GBM paths
    # np.random.seed(42)
    for t in range(1, T):
        Z = np.random.randn(num_stocks, n_sim)  # Independent normal variables
        Z_corr = L @ Z  # Apply correlation
        drift = (mu - 0.5 * sigma**2) * dt
        diffusion = sigma.values[:, None] * np.sqrt(dt) * Z_corr
        paths[t] = paths[t - 1] * np.exp(drift.values[:, None] + diffusion)

    print("Monte Carlo Simulation Completed! ✅")

    # Compute portfolio paths
    portfolio = np.zeros((T, n_sim))


    for n in range(num_stocks):
        portfolio = portfolio + stock_qty[n] * paths[:, n, :]

    portfolio = pd.DataFrame(np.round(portfolio, 2))

    return portfolio

    # 0.7 * paths[:, 0, :] + 0.3 * paths[:, 1, :]


def plot_mc_gbm(df, num_lines=50):

    df = df / 1000

    # colors = cm.Purples(np.linspace(0.4, 0.9, num_lines))
    colors_purple = [cm.Purples(i) for i in np.linspace(0.4, 0.9, num_lines // 2)]
    colors_pink = [cm.RdPu(i) for i in np.linspace(0.4, 0.9, num_lines // 2)]
    colors = colors_purple + colors_pink

    fig, (ax1, ax2) = plt.subplots(ncols=2, sharey=True, figsize=(8, 6), gridspec_kw={'width_ratios': [3, 1]})
    # Remove borders between subplots
    plt.subplots_adjust(wspace=-0.1)

    for line_n in range(num_lines):
        ax1.plot(df.iloc[:, line_n], color=colors[line_n], alpha=0.6)  # First 10 gold simulations
    
    ax1.spines['right'].set_visible(False) 
    ax1.set_xlabel("Qtr")
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, ha='right')
    ax1.set_ylabel("Value in Thousands (₹)")
    ax1.set_title("Quarterly Simulated Prices for Portfolio")

    sns.kdeplot(y=df.iloc[-1, :num_lines], ax=ax2, color='purple', fill=True, alpha=0.3, bw_adjust=0.5)
    # Adjust x-limits so KDE starts after line plot
    ax2.spines['left'].set_visible(False)
    # ax2.hlines(df.iloc[:, -1].mean(), 0, 0.0005, color='purple')
    ax2.set_xticks([])

    # plt.title(f"Quarterly Simulated Prices for Portfolio")
    # plt.xlabel("Days")
    # plt.ylabel("Price")
    
    return fig 
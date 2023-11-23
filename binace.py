import requests
import json
import matplotlib.pyplot as plt
import pandas as pd

import ta

# Calculează RSI-ul prețurilor
def compute_rsi(prices):
    rsi_period = 14
    rsi = ta.momentum.RSIIndicator(close=pd.Series(prices), window=rsi_period, fillna=False).rsi()
    return rsi



# Calculează MACD-ul prețurilor
def compute_macd(prices):
    macd_period_short = 12
    macd_period_long = 26
    macd_period_signal = 9
    macd = ta.trend.MACD(close=pd.Series(prices), window_slow=macd_period_long, window_fast=macd_period_short, window_sign=macd_period_signal, fillna=False)
    return macd.macd(), macd.macd_signal(), macd.macd_diff()


# Obține banda inferioară, banda superioară și banda medie Bollinger
def get_bollinger_bands(prices, window_size, num_std):
    rolling_mean = prices.rolling(window=window_size).mean()
    rolling_std = prices.rolling(window=window_size).std()
    upper_band = rolling_mean + (rolling_std * num_std)
    lower_band = rolling_mean - (rolling_std * num_std)
    return upper_band, lower_band, rolling_mean


# Obține valorile Oscilatorului Stochastic
def get_stochastic_oscillator(prices, k_period, d_period):
    min_prices = prices.rolling(window=k_period).min()
    max_prices = prices.rolling(window=k_period).max()
    k_values = 100 * ((prices - min_prices) / (max_prices - min_prices))
    d_values = k_values.rolling(window=d_period).mean()
    return k_values, d_values
    
    
# Obține cheia API de la Coinbase
api_key = 'INSERT_YOUR_API_KEY_HERE'

# URL-ul API-ului Coinbase pentru prețurile Bitcoin
url = 'https://api.coinbase.com/v2/prices/BTC-USD/historic?period=all'

# Obține datele prețurilor de la API
response = requests.get(url, headers={'Authorization': 'Bearer ' + api_key})
data = json.loads(response.text)

# Extrage datele prețurilor din răspunsul API
prices = []
for price in data['data']['prices']:
    prices.append(float(price['price']))

print(prices)
# Creează un grafic al prețurilor Bitcoin
plt.plot(prices)
plt.xlabel('Data')
plt.ylabel('Preț')
plt.title('Prețurile Bitcoin în USD')
plt.show()


# Calculează media mobilă a prețurilor
window_size = 20
rolling_mean = pd.Series(prices).rolling(window_size).mean()

# Afiseaza graficul cu prețurile și media mobilă
plt.plot(prices, label='Preț')
plt.plot(rolling_mean, label='Media mobilă')
plt.legend()
plt.xlabel('Minute')
plt.ylabel('Preț')
plt.title('Prețurile Bitcoin în USD')
plt.show()

# Calculează RSI-ul prețurilor
rsi = compute_rsi(prices)

# Afiseaza graficul cu prețurile, media mobilă și RSI-ul
fig, ax = plt.subplots()
ax.plot(prices, color='b', label='Preț')
ax.plot(rolling_mean, color='g', label='Media mobilă')
ax.set_xlabel('Minute')
ax.set_ylabel('Preț')
ax.set_title('Prețurile Bitcoin în USD')
ax2 = ax.twinx()
ax2.plot(rsi, color='r', label='RSI')
ax2.set_ylabel('RSI')
ax2.set_ylim(0, 100)
fig.legend(loc="upper left", bbox_to_anchor=(0,1), bbox_transform=ax.transAxes)
plt.show()

# Calculează MACD-ul prețurilor
macd, macd_signal, macd_hist = compute_macd(prices)

# Afiseaza graficul cu prețurile, media mobilă, RSI și MACD
fig, ax = plt.subplots()
ax.plot(prices, color='b', label='Preț')
ax.plot(rolling_mean, color='g', label='Media mobilă')
ax.set_xlabel('Minute')
ax.set_ylabel('Preț')
ax.set_title('Prețurile Bitcoin în USD')
ax2 = ax.twinx()
ax2.plot(rsi, color='r', label='RSI')
ax2.set_ylabel('RSI')
ax2.set_ylim(0, 100)
ax3 = ax.twinx()
ax3.spines.right.set_position(("axes", 1.1))
ax3.bar(range(len(macd_hist)), macd_hist, color='gray', width=0.4, align='center', label='MACD Histogram')
ax3.plot(macd, color='blue', label='MACD')
ax3.plot(macd_signal, color='red', label='MACD Signal')
ax3.set_ylabel('MACD')
fig.legend(loc="upper left", bbox_to_anchor=(0,1), bbox_transform=ax.transAxes)
plt.show()



# Obține semnale de tranzacționare în funcție de semnalele MACD
def get_signals2(macd, macd_signal, prices):
    signals = []
    for i in range(0, len(macd)):
        if macd[i] > macd_signal[i] and macd[i-1] < macd_signal[i-1]:
            signals.append('buy')
        elif macd[i] < macd_signal[i] and macd[i-1] > macd_signal[i-1]:
            signals.append('sell')
        else:
            signals.append('')
    return pd.DataFrame({'signals': signals}, index=prices.index.tolist())
    #return pd.DataFrame(signals, index=prices.index, columns=["signals"])

def get_signals1(macd, macd_signal, prices):
    signals = []
    for i in range(len(macd)):
        if i == 0:
            signals.append('')
            continue
        if macd[i] > macd_signal[i] and macd[i-1] < macd_signal[i-1]:
            signals.append('buy')
        elif macd[i] < macd_signal[i] and macd[i-1] > macd_signal[i-1]:
            signals.append('sell')
        else:
            signals.append('')
    return pd.DataFrame({'signals': signals}, index=prices.index)

# Obține semnale de tranzacționare în funcție de semnalele MACD
def get_signals(macd, macd_signal, prices):
    signals = []
    for i in range(0, len(macd)):
        if macd[i] > macd_signal[i] and macd[i-1] < macd_signal[i-1]:
            signals.append('buy')
        elif macd[i] < macd_signal[i] and macd[i-1] > macd_signal[i-1]:
            signals.append('sell')
        else:
            signals.append('')
    return signals


# convert the list to a pandas series
prices_series = pd.Series(prices)

# get the index of the series
index = prices_series.index.tolist()

# pass the index to the DataFrame constructor
dfp = pd.DataFrame({'prices': prices}, index=index)

# Obține semnalele de tranzacționare în funcție de semnalele MACD
signals = get_signals(macd, macd_signal, dfp)

# Afiseaza graficul cu prețurile, media mobilă, RSI, MACD și semnale
fig, ax = plt.subplots()
ax.plot(prices, color='b', label='Preț')
ax.plot(rolling_mean, color='g', label='Media mobilă')
ax.set_xlabel('Minute')
ax.set_ylabel('Preț')
ax.set_title('Prețurile Bitcoin în USD')
ax2 = ax.twinx()
ax2.plot(rsi, color='r', label='RSI')
ax2.set_ylabel('RSI')
ax2.set_ylim(0, 100)
ax3 = ax.twinx()
ax3.spines.right.set_position(("axes", 1.1))
ax3.bar(range(len(macd_hist)), macd_hist, color='gray', width=0.4, align='center', label='MACD Histogram')
ax3.plot(macd, color='blue', label='MACD')
ax3.plot(macd_signal, color='red', label='MACD Signal')
ax3.set_ylabel('MACD')
# Adaugă semnalele la grafic
for i in range(len(signals)):
    if signals[i] == 'buy':
        ax.annotate('buy', xy=(i, prices[i]), xytext=(i, prices[i]+500), arrowprops=dict(facecolor='green', shrink=0.05))
    elif signals[i] == 'sell':
        ax.annotate('sell', xy=(i, prices[i]), xytext=(i, prices[i]-500), arrowprops=dict(facecolor='red', shrink=0.05))
fig.legend(loc="upper left", bbox_to_anchor=(0,1), bbox_transform=ax.transAxes)
plt.show()



# # Obține banda inferioară, banda superioară și banda medie Bollinger

# # Transformă lista prices într-un obiect DataFrame
prices_df = pd.DataFrame(prices, columns=['price'])
# upper_band, lower_band, rolling_mean = get_bollinger_bands(prices_df, window_size=20, num_std=2)

# # Obține benzile Bollinger
sma = prices_df.rolling(window=20).mean()
std = prices_df.rolling(window=20).std()
upper_band = sma + (2 * std)
lower_band = sma - (2 * std)

# # Obține semnalele de cumpărare și vânzare pe baza benzilor Bollinger
# signals = []
# for i in range(len(prices)):
    # if prices_df[i] > upper_band[i]:
        # signals.append('sell')
    # elif prices_df[i] < lower_band[i]:
        # signals.append('buy')
    # else:
        # signals.append('hold')

# # Afiseaza graficul cu prețurile, media mobilă, RSI, MACD, benzile Bollinger și semnale
# fig, ax = plt.subplots()
# ax.plot(prices, color='b', label='Preț')
# ax.plot(sma, color='g', label='Media mobilă')
# ax.plot(upper_band, '--', color='r', label='Banda superioară Bollinger')
# ax.plot(lower_band, '--', color='r', label='Banda inferioară Bollinger')
# ax.set_xlabel('Minute')
# ax.set_ylabel('Preț')
# ax.set_title('Prețurile Bitcoin în USD')
# ax2 = ax.twinx()
# ax2.plot(rsi, color='r', label='RSI')
# ax2.set_ylabel('RSI')
# ax2.set_ylim(0, 100)
# ax3 = ax.twinx()
# ax3.spines.right.set_position(("axes", 1.1))
# ax3.bar(range(len(macd_hist)), macd_hist, color='gray', width=0.4, align='center', label='MACD Histogram')
# ax3.plot(macd, color='blue', label='MACD')
# ax3.plot(macd_signal, color='red', label='MACD Signal')
# ax3.set_ylabel('MACD')
# # Adaugă semnalele la grafic
# for i in range(len(signals)):
    # if signals[i] == 'buy':
        # ax.axvline(x=signals.index[i], color='g', linestyle='--')
    # elif signals[i] == 'sell':
        # ax.axvline(x=signals.index[i], color='r', linestyle='--')
# plt.show()



# Transformă lista prices într-un obiect DataFrame
prices_df = pd.DataFrame(prices, columns=['price'])

# Calculează Oscilatorul Stochastic
low_min = prices_df['price'].rolling(window=14).min()
high_max = prices_df['price'].rolling(window=14).max()
k_percent = 100 * ((prices_df['price'] - low_min) / (high_max - low_min))
d_percent = k_percent.rolling(window=3).mean()


# # Obține valorile Oscilatorului Stochastic
# k_values, d_values = get_stochastic_oscillator(prices, k_period=14, d_period=3)

# # Afiseaza graficul cu prețurile, media mobilă, RSI, MACD, benzile Bollinger, Oscilatorul Stochastic și semnale
# fig, ax = plt.subplots()
# ax.plot(prices, color='b', label='Preț')
# ax.plot(rolling_mean, color='g', label='Media mobilă')
# ax.plot(upper_band, '--', color='r', label='Banda superioară Bollinger')
# ax.plot(lower_band, '--', color='r', label='Banda inferioară Bollinger')
# ax.set_xlabel('Minute')
# ax.set_ylabel('Preț')
# ax.set_title('Prețurile Bitcoin în USD')
# ax2 = ax.twinx()
# ax2.plot(rsi, color='r', label='RSI')
# ax2.set_ylabel('RSI')
# ax2.set_ylim(0, 100)
# ax3 = ax.twinx()
# ax3.spines.right.set_position(("axes", 1.1))
# ax3.bar(range(len(macd_hist)), macd_hist, color='gray', width=0.4, align='center', label='MACD Histogram')
# ax3.plot(macd, color='blue', label='MACD')
# ax3.plot(macd_signal, color='red', label='MACD Signal')
# ax3.set_ylabel('MACD')
# ax4 = ax.twinx()
# ax4.spines.right.set_position(("axes", 1.2))
# ax4.plot(k_values, '--', color='b', label='Stochastic K')
# ax4.plot(d_values, '--', color='r', label='Stochastic D')
# ax4.set_ylabel('Stochastic Oscillator')
# # Adaugă semnalele la grafic
# for i in range(len(signals)):
    # if signals[i] == 'buy':
        # ax.axvline(x=signals.index[i], color='g', linestyle='--')
    # elif signals[i] == 'sell':
        # ax.axvline(x=signals.index[i], color='r', linestyle='--')
# plt.show()



# Generează semnalele de cumpărare și vânzare pe baza Oscilatorului Stochastic
signals = []
for i in range(len(prices)):
    if k_percent[i] > d_percent[i]:
        signals.append('buy')
    elif k_percent[i] < d_percent[i]:
        signals.append('sell')
    else:
        signals.append('hold')

# Afiseaza graficul cu prețurile, media mobilă, RSI, MACD, oscilatorul Stochastic și semnale
fig, ax = plt.subplots()
ax.plot(prices, color='b', label='Preț')
ax.plot(sma, color='g', label='Media mobilă')
ax.set_xlabel('Minute')
ax.set_ylabel('Preț')
ax.set_title('Prețurile Bitcoin în USD')
ax2 = ax.twinx()
ax2.plot(rsi, color='r', label='RSI')
ax2.set_ylabel('RSI')
ax2.set_ylim(0, 100)
ax3 = ax.twinx()
ax3.spines.right.set_position(("axes", 1.1))
ax3.bar(range(len(macd_hist)), macd_hist, color='gray', width=0.4, align='center', label='MACD Histogram')
ax3.plot(macd, color='blue', label='MACD')
ax3.plot(macd_signal, color='red', label='MACD Signal')
ax3.set_ylabel('MACD')
ax4 = ax.twinx()
ax4.plot(k_percent, color='purple', label='Oscilatorul Stochastic %K')
ax4.plot(d_percent, color='orange', label='Oscilatorul Stochastic %D')
ax4.set_ylabel('Oscilatorul Stochastic')
# Adaugă semnalele la grafic
#signals.reset_index(inplace=True)
signals_df = pd.DataFrame({'signals': signals}, index=prices_df.index)
for i in range(len(signals)):
    if signals[i] == 'buy':
        ax.axvline(x=signals_df.index[i], color='g', linestyle='--')
    elif signals[i] == 'sell':
        #ax.axvline(x=signals.index[i], color='r', linestyle='--')
        ax.axvline(x=signals_df.index[i], color='r', linestyle='--')

plt.show()

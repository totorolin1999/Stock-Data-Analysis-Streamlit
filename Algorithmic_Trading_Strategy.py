import datetime as dt
import matplotlib.pyplot as plt
import pandas_datareader as web
import streamlit as st

plt.style.use("dark_background")

start = dt.datetime.now() - dt.timedelta(days=365 * 3)
end = dt.datetime.now()

st.title('Algorithmic Trading Strategy')

user_input = st.text_input('Enter Stock Ticker', '2330.TW')
data = web.DataReader(user_input, 'yahoo', start, end)

#Describing Data
st.subheader(f'Data from {start} - {end}')
st. write(data.describe())

#Visualizations
st.subheader('Closing Price vs Time chart')
fig = plt.figure(figsize = (12,6))
plt.plot(data.Close)
st.pyplot(fig)

ma_1 = 30
ma_2 = 100

st.subheader(f'Closing Price vs Time chart with {ma_1}MA')
ma1 = data.Close.rolling(window=ma_1).mean()
fig = plt.figure(figsize = (12,6))
plt.plot(ma1)
plt.plot(data.Close)
st.pyplot(fig)


st.subheader(f'Closing Price vs Time chart with {ma_1}MA & {ma_2}MA')
ma1 = data.Close.rolling(window=ma_1).mean()
ma2 = data.Close.rolling(window=ma_2).mean()
fig = plt.figure(figsize = (12,6))
plt.plot(ma1, 'r')
plt.plot(ma2, 'g')
plt.plot(data.Close, 'b')
st.pyplot(fig)


data[f'SMA_{ma_1}'] = data['Adj Close'].rolling(window=ma_1).mean() # f-string 字串格式化
data[f'SMA_{ma_2}'] = data['Adj Close'].rolling(window=ma_2).mean()

data = data.iloc[ma_2:] # iloc[]是用index位置來取我們要的資料。

plt.plot(data['Adj Close'], label="Share Price", color="Lightgray")
plt.plot(data[f'SMA_{ma_1}'], label=f'SMA_{ma_1}', color="orange")
plt.plot(data[f'SMA_{ma_2}'], label=f'SMA_{ma_2}', color="purple")
plt.legend(loc="upper left")
plt.show()

buy_signals = [] # 產生一個名叫buy_signals的list
sell_signals = [] # 產生一個名叫sell_signals的list
trigger = 0 # trigger先設為0

for x in range(len(data)): # 參數設為data筆數
    if data[f'SMA_{ma_1}'].iloc[x] > data[f'SMA_{ma_2}'].iloc[x] and trigger != 1: # 如果data中的SMA_ma_1大於SMA_ma_2且trigger不等於1
        buy_signals.append(data['Adj Close'].iloc[x]) #  buy_signals增加data中該筆資料的Adj Close
        sell_signals.append(float('nan')) #  sell_signals增加一個浮點數為nan
        trigger = 1 # trigger更為1
    elif data[f'SMA_{ma_1}'].iloc[x] < data[f'SMA_{ma_2}'].iloc[x] and trigger != -1:
        buy_signals.append(float('nan'))
        sell_signals.append(data['Adj Close'].iloc[x])
        trigger = -1 # trigger更為-1
    else:
        buy_signals.append(float('nan'))
        sell_signals.append(float('nan'))

data['Buy Signals'] = buy_signals
data['Sell Signals'] = sell_signals

st.subheader('Algorithmic Trading Strategy')
fig = plt.figure(figsize = (12,6))
plt.plot(data['Adj Close'], label="Share Price", alpha=0.5)
plt.plot(data[f'SMA_{ma_1}'], label=f"SMA_{ma_1}", color="orange", linestyle="--")
plt.plot(data[f'SMA_{ma_2}'], label=f"SMA_{ma_2}", color="pink", linestyle="--")
plt.scatter(data.index, data['Buy Signals'], label="Buy signal", marker="^", color="#00ff00", lw=3)
plt.scatter(data.index, data['Sell Signals'], label="Sell signal", marker="v", color="#ff0000", lw=3)
plt.legend(loc="upper left")
st.pyplot(fig)
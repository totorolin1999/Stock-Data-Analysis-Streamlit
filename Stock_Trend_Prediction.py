import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as data
from keras.models import load_model
import streamlit as st
import datetime as dt

plt.style.use("dark_background")

start = dt.datetime.now() - dt.timedelta(days=365 * 3)
end = dt.datetime.now()

st.title('Stock Trend Prediction')

user_input = st.text_input('Enter Stock Ticker', '2330.TW')
df = data.DataReader(user_input, 'yahoo', start, end)

#Describing Data
st.subheader(f'Data from {start} - {end}')
st. write(df.describe())

#Visualizations
st.subheader('Closing Price vs Time chart')
fig = plt.figure(figsize = (12,6))
plt.plot(df.Close)
st.pyplot(fig)

ma_1 = 30
ma_2 = 100

st.subheader(f'Closing Price vs Time chart with {ma_1}MA')
ma1 = df.Close.rolling(window=ma_1).mean()
fig = plt.figure(figsize = (12,6))
plt.plot(ma1)
plt.plot(df.Close)
st.pyplot(fig)


st.subheader(f'Closing Price vs Time chart with {ma_1}MA & {ma_2}MA')
ma1 = df.Close.rolling(window=ma_1).mean()
ma2 = df.Close.rolling(window=ma_2).mean()
fig = plt.figure(figsize = (12,6))
plt.plot(ma1, 'r')
plt.plot(ma2, 'g')
plt.plot(df.Close, 'b')
st.pyplot(fig)


# Splitting Data into Training and Testing

data_training = pd.DataFrame(df['Close'][0:int(len(df)*0.70)])
data_testing = pd.DataFrame(df['Close'][int(len(df)*0.70): int(len(df))])

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0,1))

data_training_array = scaler.fit_transform(data_training)



#Load my model
model = load_model('keras_model.h5')

#Testing Part

past_100_days = data_training.tail(100)
final_df = past_100_days.append(data_testing, ignore_index=True)
input_data = scaler.fit_transform(final_df)

x_test = [] # 產生一個名叫x_test的list
y_test = [] # 產生一個名叫y_test的list

for i in range(100, data_training_array.shape[0]):
    x_test.append(data_training_array[i-100: i])
    y_test.append(data_training_array[i, 0])

x_test, y_test = np.array(x_test), np.array(y_test)
y_predicted = model.predict(x_test)
scaler = scaler.scale_

scaler_factor = 1/scaler[0]
y_predicted = y_predicted * scaler_factor
y_test = y_test * scaler_factor


#Final Graph

st.subheader('Predictions vs Original')
fig2 = plt.figure(figsize=(12,6))
plt.plot(y_test, 'b', label = 'Original Price')
plt.plot(y_predicted, 'r', label = 'Predicted Price')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
st.pyplot(fig2)
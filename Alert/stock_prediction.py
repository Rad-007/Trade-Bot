import yfinance as yf
import pandas as pd

# Define the stock symbol and the date range
stock_symbol = "WIPRO.NS"
start_date = "2020-08-31"  # Replace with your desired start date
end_date = "2023-08-31"    # Replace with your desired end date

# Fetch historical data from Yahoo Finance
stock_data = yf.download(stock_symbol, start=start_date, end=end_date)

# Save the data to a CSV file
stock_data.to_csv(f"{stock_symbol.replace('.NS','')}.csv")

# Display the first few rows of the data
#print(stock_data.head())

import pandas as pd

# Load historical stock data from the CSV file
stock_data = pd.read_csv(f"{stock_symbol.replace('.NS','')}.csv", index_col="Date")

# Display the first few rows of the data
stock_data.head()
'''Plot data 
import matplotlib.dates as mdates

import matplotlib.pyplot as plt

import datetime as dt

plt.figure(figsize=(15,10))

plt.gca().xaxis. set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gca().xaxis. set_major_locator(mdates.DayLocator (interval=30))
x_dates = [dt.datetime.strptime(d, '%Y-%m-%d').date() for d in stock_data.index.values]
plt.plot(x_dates, stock_data['High'], label='High')
plt.plot(x_dates, stock_data['Low'], label='Low')

plt.xlabel('Time Scale')

plt.ylabel('scaled Ruppee')

plt.legend()
 
plt.gcf().autofmt_xdate()

plt. show()

'''
import matplotlib.pyplot as plt 
import pandas as pd 
import numpy as np 
from tensorflow.keras.models import Sequential 
from tensorflow.keras.layers import Dense 
from tensorflow.keras.layers import LSTM 
from tensorflow.keras.layers import Dropout 
from tensorflow.keras.layers import * 
from tensorflow.keras.callbacks import EarlyStopping 

from sklearn.preprocessing import MinMaxScaler, StandardScaler 
from sklearn.metrics import mean_squared_error 
from sklearn.metrics import mean_absolute_percentage_error 
from sklearn.model_selection import train_test_split ,TimeSeriesSplit 
from sklearn.metrics import mean_squared_error


target_y = stock_data['Close']
X_feat = stock_data.iloc[:,0:3]

sc = StandardScaler()
X_ft = sc.fit_transform(X_feat.values)
X_ft = pd.DataFrame(columns=X_feat.columns,data=X_ft,index=X_feat.index)

def lstm_split (data, n_steps) : 
    X, y = [], [] 
    for i in range (len (data)-n_steps+1) : 
        X.append(data[i : i + n_steps, : -1]) 
        y.append(data[i+n_steps-1, -1]) 
    return np.array(X), np.array(y)

X1, y1 = lstm_split(stock_data.values, n_steps=2)

train_split=0.8

split_idx = int(np.ceil(len(X1)*train_split))

date_index = stock_data.index

X_train, X_test = X1[:split_idx], X1[split_idx:]

y_train, y_test = y1[:split_idx], y1[split_idx:]

X_train_date, X_test_date = date_index[:split_idx], date_index[split_idx:]


print(X1.shape, X_train.shape, X_test.shape, y_test.shape)


lstm = Sequential()

lstm.add(LSTM(32, input_shape=(X_train.shape[1], X_train.shape[2]),activation='relu', return_sequences=True))

lstm.add(Dense(1))

lstm.compile(loss='mean_squared_error', optimizer='adam')

lstm. summary()

history=lstm.fit(X_train, y_train,epochs=100, batch_size=4,verbose=2, shuffle=False)


y_pred = lstm.predict(X_test)

y_pred=y_pred.reshape(-1)
y_test=y_test.reshape(-1)

print(np.shape(y_pred))
print(np.shape(y_test))

rmse = mean_squared_error(y_test[:149], y_pred[:149], squared=False)
mape = mean_absolute_percentage_error(y_test[:149], y_pred[:149])
print("RSME: ",rmse)

print("MAPE: ", mape)


lstm = Sequential()

lstm.add(LSTM(50, input_shape=(X_train.shape[1], X_train.shape[2]),
activation='relu', return_sequences=True))

lstm.add(LSTM(50, activation='relu'))

lstm.add(Dense(1))

lstm.compile(loss='mean_squared_error', optimizer='adam')

lstm.summary ()


rmse = mean_squared_error(y_test[:149], y_pred[:149], squared=False)
mape = mean_absolute_percentage_error(y_test[:149], y_pred[:149])
print("RSME: ",rmse)

print("MAPE: ", mape)



n_steps=10

X1, y1 = lstm_split(stock_data.values, n_steps=n_steps)

train_split=0.8

split_idx = int(np.ceil(len(X1)*train_split))

date_index = stock_data.index

X_train, X_test = X1[:split_idx], X1[split_idx:]

y_train, y_test = y1[:split_idx], y1[split_idx:]

X_train_date, X_test_date = date_index[:split_idx], date_index[split_idx:-n_steps]
print(X1.shape, X_train.shape, X_test.shape, X_test_date.shape, y_test.shape)


rmse = mean_squared_error(y_test, y_pred, squared=False)
mape = mean_absolute_percentage_error(y_test, y_pred)
print("RSME: ",rmse)

print("MAPE: ", mape)


train_split = 0.8

split_idx = int(np.ceil(len(stock_data)*train_split))

train = stock_data[['Close']].iloc[:split_idx]

test = stock_data[['Close']].iloc[split_idx:]

test_pred = np.array([train.rolling(10).mean().iloc[-1]]*len(test)).reshape((-1,1))
print('Test RMSE: %.3f' % mean_squared_error(test, test_pred, squared=False))
print('Test MAPE: %.3f' % mean_absolute_percentage_error(test, test_pred))
plt.figure(figsize=(10,5))

plt.plot(test)

plt.plot(test_pred)

plt.show()



from statsmodels.tsa.api import SimpleExpsmoothing
X = stock_data[['Close']].values
train_split = 0.8
split_idx = int(np.ceil(len(X)*train_split))
train = X[:split_idx]
test = X[split_idx:]
test_concat = np.array([]).reshape((0,1))
for i in range(len(test)):
    train_fit = np.concatenate((train, np.asarray(test_concat)))
    fit = SimpleExpsmoothing(np.asarray(train_fit)).fit(smoothing_level=0.2)
    test_pred = fit.forecast(1)
    test_concat = np.concatenate((np.asarray(test_concat), test_pred.reshape((-1,1))))
print('Test RMSE: %.3f' % mean_squared_error(test, test_concat, squared=False))
print('Test MAPE: %.3f' % mean_absolute_percentage_error(test, test_concat))

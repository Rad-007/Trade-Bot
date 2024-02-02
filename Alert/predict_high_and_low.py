import yfinance as yf
import pandas as pd
from catboost import CatBoostRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np

# Function to fetch historical data for a stock
def fetch_historical_data(stock_symbol, start_date, end_date):
    try:
        stock_data = yf.download(stock_symbol, start=start_date, end=end_date)
        return stock_data
    except Exception as e:
        print(f"Error fetching data for {stock_symbol}: {str(e)}")
        return None






# Function to predict today's high price using CatBoost
def predict_today_high(stock_data):
    # Prepare the data
    stock_data['Date'] = stock_data.index
    stock_data['Date'] = pd.to_datetime(stock_data['Date'])
    stock_data['Day_of_Week'] = stock_data['Date'].dt.dayofweek
    stock_data['Month'] = stock_data['Date'].dt.month
    stock_data['Year'] = stock_data['Date'].dt.year
    stock_data['Day'] = stock_data['Date'].dt.day
    stock_data['Week_Number'] = stock_data['Date'].dt.strftime('%U').astype(int)

    # Features and target variable
    features = ['Open', 'Low', 'Volume', 'Day_of_Week', 'Month', 'Year', 'Day', 'Week_Number']
    target = 'High'

    # Split data into training and testing sets
    X = stock_data[features]
    y = stock_data[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

    # Initialize and train the CatBoost regressor
    model = CatBoostRegressor(iterations=1000, depth=6, learning_rate=0.1, loss_function='RMSE')
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Calculate RMSE (Root Mean Squared Error) on the test set
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    print(f"RMSE: {rmse}")

    # Predict today's high price (use the last row of data)
    last_row = X.tail(1)
    today_high_prediction = model.predict(last_row)
    return today_high_prediction[0]


from datetime import datetime,timedelta


def predict_high(stock_symbol):
    
    today_date = datetime.now().date()
    start_date = today_date - timedelta(days=60)  # 60 days ago
    end_date = today_date


# Fetch historical data
    stock_data = fetch_historical_data(stock_symbol, start_date, end_date)

    if stock_data is not None:
        # Predict today's high price
        today_high_prediction = predict_today_high(stock_data)
        print(f"Predicted today's high price for {stock_symbol}: {today_high_prediction:.2f}")
        return(today_high_prediction)
    else:
        print("Failed to fetch historical data.")
        return(0)
    


#--------------------------------------------------------------------------------------------------------#
# Function to predict today's high price using CatBoost



def predict_today_low(stock_data):
    # Prepare the data
    stock_data['Date'] = stock_data.index
    stock_data['Date'] = pd.to_datetime(stock_data['Date'])
    stock_data['Day_of_Week'] = stock_data['Date'].dt.dayofweek
    stock_data['Month'] = stock_data['Date'].dt.month
    stock_data['Year'] = stock_data['Date'].dt.year
    stock_data['Day'] = stock_data['Date'].dt.day
    stock_data['Week_Number'] = stock_data['Date'].dt.strftime('%U').astype(int)

    # Features and target variable
    features = ['Open', 'High', 'Volume', 'Day_of_Week', 'Month', 'Year', 'Day', 'Week_Number']
    target = 'Low'

    # Split data into training and testing sets
    X = stock_data[features]
    y = stock_data[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

    # Initialize and train the CatBoost regressor
    model = CatBoostRegressor(iterations=1000, depth=6, learning_rate=0.1, loss_function='RMSE')
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Calculate RMSE (Root Mean Squared Error) on the test set
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    print(f"RMSE: {rmse}")

    # Predict today's high price (use the last row of data)
    last_row = X.tail(1)
    today_low_prediction = model.predict(last_row)
    return today_low_prediction[0]


from datetime import datetime,timedelta


def predict_low(stock_symbol):
    
    today_date = datetime.now().date()
    start_date = today_date - timedelta(days=60)  # 60 days ago
    end_date = today_date


# Fetch historical data
    stock_data = fetch_historical_data(stock_symbol, start_date, end_date)

    if stock_data is not None:
        # Predict today's high price
        today_low_prediction = predict_today_low(stock_data)
        print(f"Predicted today's low price for {stock_symbol}: {today_low_prediction:.2f}")
        return(today_low_prediction)
    else:
        print("Failed to fetch historical data.")
        return(0)
    



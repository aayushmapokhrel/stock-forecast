from sklearn.linear_model import LinearRegression
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

def train_model(df):
    """
    Train Linear Regression using lag features
    """
    feature_cols = [col for col in df.columns if "lag" in col]
    X = df[feature_cols]
    y = df["close"]
    
    model = LinearRegression()
    model.fit(X, y)
    return model

def predict_next_day(model, df):
    """
    Predict next day's closing price
    """
    last_row = df.iloc[-1:]
    feature_cols = [col for col in df.columns if "lag" in col]
    next_day_pred = model.predict(last_row[feature_cols])[0]
    return next_day_pred

def plot_trend(df):
    plt.figure(figsize=(10,5))
    plt.plot(df["date"], df["close"], label="Actual Close")
    plt.xlabel("Date")
    plt.ylabel("Close Price")
    plt.title("Stock Price Trend")
    plt.legend()
    
    # Save plot as base64
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    plt.close()
    return img_base64

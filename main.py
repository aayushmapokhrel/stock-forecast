from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
import pandas as pd

from app.database import Base, engine, get_db
from app.models import StockPrice
from app.schemas import StockPriceCreate, StockPrediction
from app.utils import create_lag_features
from app.predictor import train_model, predict_next_day, plot_trend
from fastapi.responses import StreamingResponse
import io
import matplotlib.pyplot as plt

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Stock Price Predictor")


# --- Add stock price data ---
@app.post("/add_stock/", response_model=StockPriceCreate)
def add_stock(stock: StockPriceCreate, db: Session = Depends(get_db)):
    db_stock = StockPrice(**stock.dict())
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock


# --- Predict next day's close ---
@app.get("/predict/", response_model=StockPrediction)
def predict(db: Session = Depends(get_db)):
    # Fetch data
    df = pd.read_sql(db.query(StockPrice).statement, db.bind)
    if len(df) < 4:
        raise HTTPException(status_code=400, detail="Not enough data to predict")

    df_lag = create_lag_features(df)
    model = train_model(df_lag)
    next_day_pred = predict_next_day(model, df_lag)

    return StockPrediction(
        date=df["date"].max() + pd.Timedelta(days=1),
        predicted_close=round(next_day_pred, 2),
    )


# --- Trend visualization ---
@app.get("/trend/")
def get_trend_img(db: Session = Depends(get_db)):
    df = pd.read_sql(db.query(StockPrice).statement, db.bind)

    plt.figure(figsize=(12, 6))

    # Plot multiple lines
    plt.plot(df["date"], df["open"], label="Open", color="blue", linestyle="--")
    plt.plot(df["date"], df["high"], label="High", color="green")
    plt.plot(df["date"], df["low"], label="Low", color="red")
    plt.plot(df["date"], df["close"], label="Close", color="black", linewidth=2)

    # Labels and title
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title("Stock Price Trend: Open, High, Low, Close")
    plt.legend()
    plt.grid(True)
    plt.savefig("image/trend_chart.png", format="png")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()

    return StreamingResponse(buf, media_type="image/png")

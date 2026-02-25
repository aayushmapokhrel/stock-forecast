from pydantic import BaseModel
from datetime import date

class StockPriceCreate(BaseModel):
    date: date
    open: float
    high: float
    low: float
    close: float
    volume: float

class StockPrediction(BaseModel):
    date: date
    predicted_close: float

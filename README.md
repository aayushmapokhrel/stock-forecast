# Stock Price Prediction

    Predict future stock prices using Machine Learning with FastAPI and PostgreSQL.
    This project demonstrates a simplified stock price prediction system using historical stock data.
    It features Linear Regression provides trend visualization, and exposes a REST API for easy integration.

## Features
    - Store historical stock data in PostgreSQL
    - Create lag features for supervised learning
    - Predict the **next day’s closing price
    - Generate trend plots for open, high, low, and close prices
    - Built with FastAPI for REST API deployment
    - Supports both in-memory charts and optional saved images
    
## Tech Stack
    - Backend/API: FastAPI  
    - Database: PostgreSQL  
    - Data Processing: Pandas, NumPy  
    - Machine Learning: scikit-learn (Linear Regression)  
    - Visualization: Matplotlib  
    
### Installation

## Clone the repository:
    git clone: https://github.com/aayushmapokhrel/stock-forecast.git

## Create a virtual environment
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows
    
## Install dependencies
    pip install -r requirements.txt

## Set up PostgreSQL database
    DATABASE_URL = "postgresql://username:password@localhost:5432/stockdb"

## Run the FastAPI app
    uvicorn app.main:app --reload
    
## Open API docs in browser
    http://127.0.0.1:8000/docs

  
    

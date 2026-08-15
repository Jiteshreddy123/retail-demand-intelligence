import os

from dotenv import load_dotenv
from fastapi import FastAPI
from google import genai

from src.analytics.metrics import (
    get_business_metrics,
    get_top_stores,
)

load_dotenv()

app = FastAPI(
    title="Retail Demand Intelligence API",
    version="1.0.0",
)

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


@app.get("/")
def root():
    return {
        "project": "Retail Demand Intelligence & Forecasting System",
        "status": "running",
    }


@app.get("/metrics")
def metrics():
    return {
        "overall": get_business_metrics(),
        "top_stores": get_top_stores(),
    }


@app.get("/insights")
def insights():
    metrics_data = get_business_metrics()
    top_stores = get_top_stores()

    context = f"""
    Overall retail metrics:
    {metrics_data}

    Top stores:
    {top_stores}

    Forecast model:
    WMAPE: 8.53%
    MAE: 1332.49
    RMSE: 2850.40
    """

    prompt = f"""
    Act as a retail business intelligence analyst.

    Analyze ONLY the following supplied information:

    {context}

    Give:
    1. Executive summary
    2. Important findings
    3. Forecast interpretation
    4. Three practical recommendations
    5. Limitations

    Do not invent data or causes.
    """

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )

    return {
        "insights": response.text
    }
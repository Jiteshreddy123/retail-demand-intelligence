import os

from dotenv import load_dotenv
from google import genai

from src.analytics.metrics import (
    get_business_metrics,
    get_top_stores,
)

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

metrics = get_business_metrics()
top_stores = get_top_stores()

business_context = f"""
Retail Demand Intelligence System

Overall metrics:
{metrics}

Top stores by total sales:
{top_stores}

Forecast model:
- Model: HistGradientBoostingRegressor
- Time-based validation
- WMAPE: 8.53%
- MAE: 1,332.49
- RMSE: 2,850.40
"""

question = """
Explain the current retail performance for a manager.

Identify important observations from the supplied numbers,
explain what the forecasting performance means,
and recommend practical areas to investigate.

Do not invent information.
"""

prompt = f"""
You are an experienced retail business intelligence analyst.

Use ONLY the supplied data.

{business_context}

Manager question:
{question}

Return:
1. Executive Summary
2. Key Findings
3. Forecast Interpretation
4. Recommended Actions
5. Limitations
"""

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt,
)

print(response.text)
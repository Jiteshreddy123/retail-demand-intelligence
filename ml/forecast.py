import pandas as pd
import numpy as np

from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error


# ---------------------------------------
# 1. Load processed data
# ---------------------------------------

df = pd.read_csv("data/processed/retail_sales_clean.csv")

df["Date"] = pd.to_datetime(df["Date"])

df = df.sort_values(["Store", "Dept", "Date"]).reset_index(drop=True)

print("Dataset:", df.shape)


# ---------------------------------------
# 2. Create time-series features
# ---------------------------------------

group = df.groupby(["Store", "Dept"])["Weekly_Sales"]

df["Lag_1"] = group.shift(1)
df["Lag_4"] = group.shift(4)
df["Lag_12"] = group.shift(12)

df["Rolling_Mean_4"] = (
    df.groupby(["Store", "Dept"])["Weekly_Sales"]
    .transform(lambda x: x.shift(1).rolling(4).mean())
)


# ---------------------------------------
# 3. Select ML features
# ---------------------------------------

features = [
    "Store",
    "Dept",
    "Year",
    "Month",
    "Week",
    "IsHoliday",
    "Temperature",
    "Fuel_Price",
    "CPI",
    "Unemployment",
    "Lag_1",
    "Lag_4",
    "Lag_12",
    "Rolling_Mean_4",
]

target = "Weekly_Sales"

model_data = df.dropna(subset=features + [target]).copy()

print("Model dataset:", model_data.shape)


# ---------------------------------------
# 4. Time-based train/test split
# ---------------------------------------

cutoff_date = model_data["Date"].max() - pd.Timedelta(weeks=12)

train = model_data[model_data["Date"] <= cutoff_date]
validation = model_data[model_data["Date"] > cutoff_date]

print("Train:", train.shape)
print("Validation:", validation.shape)

X_train = train[features]
y_train = train[target]

X_valid = validation[features]
y_valid = validation[target]


# ---------------------------------------
# 5. Train model
# ---------------------------------------

model = HistGradientBoostingRegressor(
    max_iter=150,
    learning_rate=0.08,
    max_leaf_nodes=31,
    random_state=42
)

print("\nTraining model...")

model.fit(X_train, y_train)

print("Training complete.")


# ---------------------------------------
# 6. Evaluate
# ---------------------------------------

predictions = model.predict(X_valid)

mae = mean_absolute_error(y_valid, predictions)

rmse = np.sqrt(
    mean_squared_error(y_valid, predictions)
)

wmape = (
    np.sum(np.abs(y_valid - predictions))
    / np.sum(np.abs(y_valid))
)

print("\nModel Performance")
print("----------------------")
print(f"MAE   : {mae:,.2f}")
print(f"RMSE  : {rmse:,.2f}")
print(f"WMAPE : {wmape:.2%}")
# ---------------------------------------
# 7. Save validation predictions
# ---------------------------------------

validation_output = validation[
    ["Store", "Dept", "Date", "Weekly_Sales"]
].copy()

validation_output["Predicted_Sales"] = predictions

validation_output.to_csv(
    "data/processed/validation_predictions.csv",
    index=False
)

print("\nPredictions saved to:")
print("data/processed/validation_predictions.csv")

validation_output["Absolute_Error"] = (
    validation_output["Weekly_Sales"]
    - validation_output["Predicted_Sales"]
).abs()

print("\nTop 10 largest prediction errors:")
print(
    validation_output
    .sort_values("Absolute_Error", ascending=False)
    .head(10)
)
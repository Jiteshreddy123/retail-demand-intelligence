import pandas as pd

# -----------------------------
# 1. Extract
# -----------------------------

train = pd.read_csv("data/raw/train.csv")
features = pd.read_csv("data/raw/features.csv")
stores = pd.read_csv("data/raw/stores.csv")

print("Train shape:", train.shape)
print("Features shape:", features.shape)
print("Stores shape:", stores.shape)


# -----------------------------
# 2. Transform - Merge datasets
# -----------------------------

merged = train.merge(
    features,
    on=["Store", "Date"],
    how="left",
    suffixes=("", "_features")
)

merged = merged.merge(
    stores,
    on="Store",
    how="left"
)


# -----------------------------
# 3. Clean duplicated column
# -----------------------------

# Keep the IsHoliday column from train
# and remove the duplicate column from features.
merged = merged.drop(columns=["IsHoliday_features"])


# -----------------------------
# 4. Handle markdown missing values
# -----------------------------

markdown_columns = [
    "MarkDown1",
    "MarkDown2",
    "MarkDown3",
    "MarkDown4",
    "MarkDown5"
]

merged[markdown_columns] = merged[markdown_columns].fillna(0)


# -----------------------------
# 5. Create useful date features
# -----------------------------

merged["Date"] = pd.to_datetime(merged["Date"])

merged["Year"] = merged["Date"].dt.year
merged["Month"] = merged["Date"].dt.month
merged["Week"] = merged["Date"].dt.isocalendar().week.astype(int)


# -----------------------------
# 6. Basic validation
# -----------------------------

print("\nMerged shape:", merged.shape)

print("\nColumns:")
print(merged.columns.tolist())

print("\nMissing values:")
print(
    merged.isna()
    .sum()
    .sort_values(ascending=False)
    .head(15)
)

print("\nSample:")
print(merged.head())

# -----------------------------
# 7. Load - Save processed data
# -----------------------------

output_path = "data/processed/retail_sales_clean.csv"

merged.to_csv(output_path, index=False)

print(f"\nProcessed data saved to: {output_path}")
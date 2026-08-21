import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score

from ml_model.data_prep import load_and_clean, COL_PRICE, COL_CITY, COL_LOCATION, COL_PROPERTY_TYPE, COL_PURPOSE, COL_BEDROOMS, COL_BATHS

DATA_PATH = "data/zameen_data.csv"
MODEL_PATH = "ml_model/price_model.joblib"
ENCODERS_PATH = "ml_model/encoders.joblib"

CATEGORICAL_COLS = [COL_CITY, COL_LOCATION, COL_PROPERTY_TYPE, COL_PURPOSE]
NUMERIC_COLS = [COL_BEDROOMS, COL_BATHS, "area_marla"]


def main():
    if not os.path.exists(DATA_PATH):
        print(f"❌ Could not find {DATA_PATH}")
        print("Download the dataset from Kaggle and save it at that path first.")
        return

    print("Loading and cleaning data...")
    df = load_and_clean(DATA_PATH)
    print(f"Loaded {len(df)} clean rows after removing bad/missing data.")

    if len(df) < 100:
        print("⚠️ Very little data after cleaning -- check your CSV / column mapping.")

    # ---- Encode categorical columns ----
    encoders = {}
    for col in CATEGORICAL_COLS:
        le = LabelEncoder()
        df[col + "_enc"] = le.fit_transform(df[col].astype(str))
        encoders[col] = le

    feature_cols = [c + "_enc" for c in CATEGORICAL_COLS] + NUMERIC_COLS
    X = df[feature_cols]
    y = df[COL_PRICE]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Training model (this may take a minute)...")
    model = RandomForestRegressor(n_estimators=200, max_depth=15, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)

    print("\n===== Model Performance =====")
    print(f"R² score        : {r2:.3f}  (closer to 1.0 is better)")
    print(f"Mean Abs. Error : PKR {mae:,.0f}  (average prediction error)")
    print("==============================\n")

    joblib.dump(model, MODEL_PATH)
    joblib.dump({"encoders": encoders, "feature_cols": feature_cols}, ENCODERS_PATH)
    print(f"✅ Model saved to {MODEL_PATH}")
    print(f"✅ Encoders saved to {ENCODERS_PATH}")


if __name__ == "__main__":
    main()

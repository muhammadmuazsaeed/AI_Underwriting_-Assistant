"""
Helpers to clean and standardize the Zameen.com Pakistan property dataset.

Expected raw columns (from the Kaggle dataset):
property_id, location_id, page_url, property_type, price, location, city,
province_name, latitude, longitude, baths, area, purpose, bedrooms,
date_added, agency, agent

NOTE: Column names can vary slightly between dataset versions.
If training fails with a KeyError, run this first to check your file:
    import pandas as pd
    df = pd.read_csv("data/zameen_data.csv")
    print(df.columns.tolist())
    print(df.head())
And adjust the column names below (COLUMN MAP section) to match.
"""

import re
import pandas as pd

# ---- COLUMN MAP: change the right-hand values if your CSV uses different names ----
COL_PRICE = "price"
COL_CITY = "city"
COL_LOCATION = "location"
COL_PROPERTY_TYPE = "property_type"
COL_PURPOSE = "purpose"
COL_BEDROOMS = "bedrooms"
COL_BATHS = "baths"
COL_AREA = "area"
COL_DATE_ADDED = "date_added"


def _parse_area_to_marla(area_value) -> float:
    """
    Zameen's "area" field is usually a string like "10 Marla", "2 Kanal", "1200 Sq. Yd.".
    This converts everything to a single unit: Marla (a common Pakistani real estate unit).

    1 Kanal = 20 Marla
    1 Marla ≈ 225 sq. ft.
    1 Sq. Yd. ≈ 9 sq. ft.  ->  1 Sq. Yd. ≈ 0.04 Marla
    """
    if pd.isna(area_value):
        return None

    text = str(area_value).strip().lower()
    match = re.search(r"([\d.]+)", text)
    if not match:
        return None
    number = float(match.group(1))

    if "kanal" in text:
        return number * 20
    if "marla" in text:
        return number
    if "sq. yd" in text or "sq yd" in text or "yard" in text:
        return number * 9 / 225
    if "sq. ft" in text or "sq ft" in text or "sqft" in text:
        return number / 225

    # Unknown unit -- assume it's already in Marla
    return number


def load_and_clean(csv_path: str) -> pd.DataFrame:
    """
    Loads the raw CSV and returns a cleaned DataFrame ready for training,
    with a standardized 'area_marla' numeric column and no missing key values.
    """
    df = pd.read_csv(csv_path)

    # Keep only the columns we actually need
    keep_cols = [
        COL_PRICE, COL_CITY, COL_LOCATION, COL_PROPERTY_TYPE,
        COL_PURPOSE, COL_BEDROOMS, COL_BATHS, COL_AREA, COL_DATE_ADDED,
    ]
    missing = [c for c in keep_cols if c not in df.columns]
    if missing:
        raise KeyError(
            f"These expected columns were not found in your CSV: {missing}\n"
            f"Your CSV's actual columns are: {df.columns.tolist()}\n"
            f"Update the COLUMN MAP at the top of ml_model/data_prep.py to match."
        )

    df = df[keep_cols].copy()

    # Standardize area
    df["area_marla"] = df[COL_AREA].apply(_parse_area_to_marla)

    # Drop rows with missing essential values
    df = df.dropna(subset=[COL_PRICE, COL_CITY, COL_BEDROOMS, COL_BATHS, "area_marla"])

    # Remove obviously bad rows (0 or negative price/area)
    df = df[(df[COL_PRICE] > 0) & (df["area_marla"] > 0)]

    # Parse date_added into a proper datetime + year column (best effort)
    df[COL_DATE_ADDED] = pd.to_datetime(df[COL_DATE_ADDED], errors="coerce")
    df["year_added"] = df[COL_DATE_ADDED].dt.year

    return df

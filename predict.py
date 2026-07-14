"""
Loads the trained model and provides a simple function to predict
a property's estimated market price given its details.
"""

import os
import joblib

MODEL_PATH = os.path.join(os.path.dirname(__file__), "price_model.joblib")
ENCODERS_PATH = os.path.join(os.path.dirname(__file__), "encoders.joblib")

_model = None
_encoders = None
_feature_cols = None


def _load():
    global _model, _encoders, _feature_cols
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                "No trained model found. Run 'python -m ml_model.train_model' first "
                "(after downloading the dataset -- see ml_model/train_model.py)."
            )
        _model = joblib.load(MODEL_PATH)
        saved = joblib.load(ENCODERS_PATH)
        _encoders = saved["encoders"]
        _feature_cols = saved["feature_cols"]


def is_model_available() -> bool:
    return os.path.exists(MODEL_PATH) and os.path.exists(ENCODERS_PATH)


def _safe_encode(encoder, value: str) -> int:
    """
    Encodes a category value. If the value was never seen during training
    (e.g. a new city/location), falls back to the most common known class.
    """
    value = str(value)
    if value in encoder.classes_:
        return int(encoder.transform([value])[0])
    # Unseen category -- fall back to class 0 (best effort)
    return 0


def predict_market_price(city: str, location: str, property_type: str, purpose: str,
                          bedrooms: int, baths: int, area_marla: float) -> float:
    """
    Returns the model's estimated market price (in PKR) for a property
    with these characteristics.
    """
    _load()

    row = {
        "city_enc": _safe_encode(_encoders["city"], city),
        "location_enc": _safe_encode(_encoders["location"], location),
        "property_type_enc": _safe_encode(_encoders["property_type"], property_type),
        "purpose_enc": _safe_encode(_encoders["purpose"], purpose),
        "bedrooms": bedrooms,
        "baths": baths,
        "area_marla": area_marla,
    }

    import pandas as pd
    X = pd.DataFrame([row])[_feature_cols]
    prediction = _model.predict(X)[0]
    return float(prediction)


def get_known_cities() -> list[str]:
    _load()
    return sorted(_encoders["city"].classes_.tolist())


def get_known_locations() -> list[str]:
    _load()
    return sorted(_encoders["location"].classes_.tolist())


def get_known_property_types() -> list[str]:
    _load()
    return sorted(_encoders["property_type"].classes_.tolist())


def get_known_purposes() -> list[str]:
    _load()
    return sorted(_encoders["purpose"].classes_.tolist())

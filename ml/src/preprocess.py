"""
preprocess.py — Data Cleaning, Validation & Encoding
=====================================================
Handles raw data ingestion, schema validation, null handling,
categorical encoding, and numeric scaling.

All fitted transformers (encoder, scaler) are persisted to disk
so the same transformations can be applied at inference time.
"""

import os
import logging
import pandas as pd
import numpy as np
import joblib
import yaml
from sklearn.preprocessing import OrdinalEncoder, StandardScaler

logger = logging.getLogger(__name__)


# ── Helpers ────────────────────────────────────────────────

def load_config(config_path: str = "ml/config.yaml") -> dict:
    """Load YAML configuration file."""
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# ── Data Loading ───────────────────────────────────────────

def load_data(path: str) -> pd.DataFrame:
    """
    Read CSV dataset from disk.

    Args:
        path: Path to the raw CSV file.

    Returns:
        Raw DataFrame with no modifications.
    """
    logger.info(f"Loading data from {path}")
    df = pd.read_csv(path, encoding="utf-8")
    logger.info(f"Loaded {len(df)} rows, {len(df.columns)} columns")
    return df


# ── Schema Validation ─────────────────────────────────────

def validate_schema(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """
    Validate that the DataFrame contains all required columns
    and the target column has no nulls.

    Args:
        df: Input DataFrame.
        config: Parsed config dict.

    Returns:
        Validated DataFrame (unchanged).

    Raises:
        ValueError: If required columns are missing or target has nulls.
    """
    required_cols = (
        config["features"]["categorical"]
        + config["features"]["numeric"]
        + [config["features"]["target"]]
    )

    missing = set(required_cols) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    target = config["features"]["target"]
    null_count = df[target].isnull().sum()
    if null_count > 0:
        raise ValueError(
            f"Target column '{target}' has {null_count} null values"
        )

    logger.info("Schema validation passed")
    return df


# ── Data Cleaning ──────────────────────────────────────────

def clean_data(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """
    Clean the dataset:
    1. Drop exact duplicate rows
    2. Strip whitespace & lowercase string columns
    3. Fill missing categorical values with 'unknown'
    4. Fill missing numeric values with column median
    5. Remove rows where target ≤ 0

    Args:
        df: Raw DataFrame.
        config: Parsed config dict.

    Returns:
        Cleaned DataFrame.
    """
    initial_len = len(df)

    # 1. Drop duplicates
    df = df.drop_duplicates()
    logger.info(f"Dropped {initial_len - len(df)} duplicate rows")

    # 2. Normalize string columns
    cat_cols = config["features"]["categorical"]
    for col in cat_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.lower()

    # 3. Fill missing categoricals
    for col in cat_cols:
        if col in df.columns:
            df[col] = df[col].replace(["nan", "none", ""], "unknown")
            df[col] = df[col].fillna("unknown")

    # 4. Fill missing numerics with median
    num_cols = config["features"]["numeric"]
    for col in num_cols:
        if col in df.columns and df[col].isnull().any():
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)
            logger.info(f"Filled {col} nulls with median={median_val}")

    # 5. Remove non-positive salary
    target = config["features"]["target"]
    before = len(df)
    df = df[df[target] > 0].reset_index(drop=True)
    logger.info(f"Removed {before - len(df)} rows with {target} <= 0")

    logger.info(f"Clean data shape: {df.shape}")
    return df


# ── Categorical Encoding ──────────────────────────────────

def encode_categoricals(
    df: pd.DataFrame,
    config: dict,
    fit: bool = True,
    encoder: OrdinalEncoder | None = None,
) -> tuple[pd.DataFrame, OrdinalEncoder]:
    """
    Encode categorical features using OrdinalEncoder.
    Tree-based models work well with ordinal encoding and
    it avoids the dimensionality explosion of one-hot encoding.

    Args:
        df: DataFrame with raw categorical columns.
        config: Parsed config dict.
        fit: If True, fit a new encoder. If False, use provided encoder.
        encoder: Pre-fitted encoder (required when fit=False).

    Returns:
        Tuple of (encoded DataFrame, fitted encoder).
    """
    cat_cols = config["features"]["categorical"]
    present_cols = [c for c in cat_cols if c in df.columns]

    if fit:
        encoder = OrdinalEncoder(
            handle_unknown="use_encoded_value",
            unknown_value=-1,
        )
        df[present_cols] = encoder.fit_transform(df[present_cols])
        # Save encoder to disk
        encoder_path = config["paths"]["encoder_path"]
        os.makedirs(os.path.dirname(encoder_path), exist_ok=True)
        joblib.dump(encoder, encoder_path)
        logger.info(f"Encoder fitted and saved to {encoder_path}")
    else:
        if encoder is None:
            raise ValueError("Must provide encoder when fit=False")
        df[present_cols] = encoder.transform(df[present_cols])
        logger.info("Applied pre-fitted encoder")

    return df, encoder


# ── Numeric Scaling ────────────────────────────────────────

def scale_numerics(
    df: pd.DataFrame,
    config: dict,
    fit: bool = True,
    scaler: StandardScaler | None = None,
) -> tuple[pd.DataFrame, StandardScaler]:
    """
    Standardize numeric features (zero mean, unit variance).
    Optional for tree models but useful if we add linear models later.

    Args:
        df: DataFrame with numeric columns.
        config: Parsed config dict.
        fit: If True, fit a new scaler. If False, use provided scaler.
        scaler: Pre-fitted scaler (required when fit=False).

    Returns:
        Tuple of (scaled DataFrame, fitted scaler).
    """
    num_cols = config["features"]["numeric"]
    present_cols = [c for c in num_cols if c in df.columns]

    if fit:
        scaler = StandardScaler()
        df[present_cols] = scaler.fit_transform(df[present_cols])
        scaler_path = config["paths"]["scaler_path"]
        os.makedirs(os.path.dirname(scaler_path), exist_ok=True)
        joblib.dump(scaler, scaler_path)
        logger.info(f"Scaler fitted and saved to {scaler_path}")
    else:
        if scaler is None:
            raise ValueError("Must provide scaler when fit=False")
        df[present_cols] = scaler.transform(df[present_cols])
        logger.info("Applied pre-fitted scaler")

    return df, scaler


# ── Orchestrator ───────────────────────────────────────────

def build_pipeline(
    config_path: str = "ml/config.yaml",
) -> tuple[pd.DataFrame, pd.Series, dict]:
    """
    End-to-end preprocessing pipeline:
    1. Load config
    2. Load raw data
    3. Validate schema
    4. Clean data
    5. Encode categoricals (fit)
    6. Scale numerics (fit)
    7. Split features / target

    Args:
        config_path: Path to the YAML config file.

    Returns:
        Tuple of (X DataFrame, y Series, config dict).
    """
    config = load_config(config_path)

    # Load & validate
    df = load_data(config["paths"]["raw_data"])
    df = validate_schema(df, config)

    # Clean
    df = clean_data(df, config)

    # Save cleaned data
    processed_path = config["paths"]["processed_data"]
    os.makedirs(os.path.dirname(processed_path), exist_ok=True)
    df.to_csv(processed_path, index=False, encoding="utf-8")
    logger.info(f"Processed data saved to {processed_path}")

    # Encode & scale
    df, _ = encode_categoricals(df, config, fit=True)
    df, _ = scale_numerics(df, config, fit=True)

    # Split X / y
    target = config["features"]["target"]
    feature_cols = config["features"]["categorical"] + config["features"]["numeric"]
    X = df[[c for c in feature_cols if c in df.columns]]
    y = df[target]

    logger.info(f"Pipeline complete -- X: {X.shape}, y: {y.shape}")
    return X, y, config

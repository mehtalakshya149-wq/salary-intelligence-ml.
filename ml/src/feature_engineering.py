"""
feature_engineering.py — Derived Feature Construction
=====================================================
Creates higher-order features from raw columns to improve
model performance. All transformations are deterministic
and reproducible.
"""

import logging
import pandas as pd
import numpy as np
import yaml

logger = logging.getLogger(__name__)


# ── Helpers ────────────────────────────────────────────────

def load_config(config_path: str = "ml/config.yaml") -> dict:
    """Load YAML configuration file."""
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# ── Experience Bins ────────────────────────────────────────

def add_experience_bins(df: pd.DataFrame) -> pd.DataFrame:
    """
    Map experience_level to ordinal numeric tiers.

    Mapping:
        entry (en) → 0
        mid (mi)   → 1
        senior (se) → 2
        executive (ex) → 3

    If already encoded numerically, bins are derived from
    quartiles of the encoded values.

    Args:
        df: DataFrame with 'experience_level' column.

    Returns:
        DataFrame with new 'experience_bin' column.
    """
    level_map = {"en": 0, "mi": 1, "se": 2, "ex": 3}

    if df["experience_level"].dtype == object:
        df["experience_bin"] = (
            df["experience_level"].str.lower().map(level_map).fillna(1)
        )
    else:
        # Already encoded — use quartile binning
        df["experience_bin"] = pd.qcut(
            df["experience_level"], q=4, labels=False, duplicates="drop"
        )

    logger.info("Added experience_bin feature")
    return df


# ── Role Clusters ──────────────────────────────────────────

def add_role_cluster(
    df: pd.DataFrame, config: dict | None = None
) -> pd.DataFrame:
    """
    Group job_title into macro-categories:
    Engineer, Analyst, Scientist, Manager, Other.

    Uses keyword matching against the cluster definitions
    in config.yaml. Falls back to 'Other' if no match.

    Args:
        df: DataFrame with 'job_title' column.
        config: Parsed config dict (optional, loaded if None).

    Returns:
        DataFrame with new 'role_cluster' column.
    """
    if config is None:
        config = load_config()

    clusters = config.get("role_clusters", {})

    def _classify(title: str) -> str:
        title_lower = str(title).lower()
        for cluster_name, keywords in clusters.items():
            if cluster_name == "Other":
                continue
            for keyword in keywords:
                if keyword in title_lower:
                    return cluster_name
        return "Other"

    # If job_title is already encoded, skip text matching
    if df["job_title"].dtype != object:
        df["role_cluster"] = 0  # Placeholder for encoded data
        logger.info("Skipped role_cluster (job_title already encoded)")
    else:
        df["role_cluster"] = df["job_title"].apply(_classify)
        logger.info("Added role_cluster feature")

    return df


# ── Remote Flag ────────────────────────────────────────────

def add_remote_flag(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create a binary flag from remote_ratio.
    1 if remote_ratio ≥ 50, else 0.

    Args:
        df: DataFrame with 'remote_ratio' column.

    Returns:
        DataFrame with new 'is_remote' column.
    """
    if "remote_ratio" in df.columns:
        df["is_remote"] = (df["remote_ratio"] >= 50).astype(int)
        logger.info("Added is_remote feature")
    else:
        logger.warning("remote_ratio not found -- skipping is_remote")

    return df


# ── Company Tier ───────────────────────────────────────────

def add_company_tier(df: pd.DataFrame) -> pd.DataFrame:
    """
    Combine company_size and company_location into a tier score.

    Logic (for string data):
        - company_size: S=1, M=2, L=3
        - location premium: US/GB/DE/CA = +2, others = +0
        - tier = size_score + location_premium

    For already-encoded data, uses a simple sum as proxy.

    Args:
        df: DataFrame with 'company_size' and 'company_location'.

    Returns:
        DataFrame with new 'company_tier' column.
    """
    premium_locations = {"us", "gb", "de", "ca", "au", "ch"}
    size_map = {"s": 1, "m": 2, "l": 3}

    if df["company_size"].dtype == object:
        size_score = df["company_size"].str.lower().map(size_map).fillna(2)
        loc_premium = (
            df["company_location"]
            .str.lower()
            .isin(premium_locations)
            .astype(int)
            * 2
        )
        df["company_tier"] = size_score + loc_premium
    else:
        # Encoded — use normalized sum as proxy
        df["company_tier"] = (
            df["company_size"].fillna(0) + df.get("company_location", 0)
        )

    logger.info("Added company_tier feature")
    return df


# ── Interaction Features ──────────────────────────────────

def add_interaction_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create interaction terms that capture combined effects:
    1. experience × remote_ratio
    2. company_tier × experience_bin (if both exist)

    Args:
        df: DataFrame with engineered features.

    Returns:
        DataFrame with new interaction columns.
    """
    # Experience × Remote Ratio
    exp_col = "experience_bin" if "experience_bin" in df.columns else "experience_level"
    if exp_col in df.columns and "remote_ratio" in df.columns:
        df["exp_x_remote"] = df[exp_col] * df["remote_ratio"]
        logger.info("Added exp_x_remote interaction")

    # Company Tier × Experience
    if "company_tier" in df.columns and "experience_bin" in df.columns:
        df["tier_x_exp"] = df["company_tier"] * df["experience_bin"]
        logger.info("Added tier_x_exp interaction")

    return df


# ── Skills Count ───────────────────────────────────────────

def add_skills_count(df: pd.DataFrame) -> pd.DataFrame:
    """
    Count the number of skills listed (comma-separated string).
    If already encoded, this gracefully returns the column as-is.

    Args:
        df: DataFrame with 'skills' column.

    Returns:
        DataFrame with new 'skills_count' column.
    """
    if "skills" in df.columns:
        if df["skills"].dtype == object:
            df["skills_count"] = (
                df["skills"]
                .fillna("")
                .apply(lambda x: len([s for s in str(x).split(",") if s.strip()]))
            )
        else:
            # Already encoded — use a log-scaled proxy
            df["skills_count"] = np.log1p(df["skills"].abs())
        logger.info("Added skills_count feature")

    return df


# ── Orchestrator ───────────────────────────────────────────

def engineer_features(
    df: pd.DataFrame,
    config: dict | None = None,
) -> pd.DataFrame:
    """
    Run all feature engineering steps in sequence.

    Pipeline order:
    1. Skills count (before encoding, if possible)
    2. Experience bins
    3. Role clusters
    4. Remote flag
    5. Company tier
    6. Interaction features

    Args:
        df: Cleaned DataFrame (pre- or post-encoding).
        config: Parsed config dict (loaded if None).

    Returns:
        DataFrame with all engineered features appended.
    """
    if config is None:
        config = load_config()

    df = add_skills_count(df)
    df = add_experience_bins(df)
    df = add_role_cluster(df, config)
    df = add_remote_flag(df)
    df = add_company_tier(df)
    df = add_interaction_features(df)

    logger.info(f"Feature engineering complete -- {len(df.columns)} total columns")
    return df

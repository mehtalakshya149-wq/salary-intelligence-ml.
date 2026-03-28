"""
story_ai.py — Human-Readable Model Explanations
==============================================
Translates mathematical SHAP values into natural language stories
that explain the 'why' behind a salary prediction.
"""

import logging
import pandas as pd
import joblib
import os
from ml.src.explainability import compute_local_shap
from ml.src.preprocess import load_config
from ml.src.predict import load_encoders

logger = logging.getLogger(__name__)

FEATURE_LABELS = {
    "experience_level": "Seniority Level",
    "company_size": "Enterprise Scale",
    "company_location": "Geographic Market",
    "remote_ratio": "Remote Flexibility",
    "skills_count": "Tech Stack Depth",
    "job_title": "Role Specialization",
    "work_year": "Market Timing"
}

def generate_story(inputs: dict, config_path: str = "ml/config.yaml") -> dict:
    """
    Computes local SHAP and generates a human-readable story.
    """
    try:
        config = load_config(config_path)
        model_dir = config["paths"]["model_dir"]
        
        # Load RF model for SHAP
        rf_model = joblib.load(os.path.join(model_dir, "random_forest.joblib"))
        
        # Load background data
        test_data = joblib.load(os.path.join(model_dir, "test_data.joblib"))
        X_test = test_data["X_test"]
        
        # Preprocess input
        from ml.src.predict import preprocess_input
        encoders = load_encoders(config)
        X_single = preprocess_input(inputs, config, encoders)
        
        # Compute SHAP
        local_shap = compute_local_shap(rf_model, X_single, X_test)
        
        base_val = local_shap["base_value"]
        pred_val = local_shap["predicted_value"]
        contributions = local_shap["contributions"]
        
        # Build Narrative
        positives = []
        negatives = []
        
        for feat, val in contributions.items():
            label = FEATURE_LABELS.get(feat, feat.replace("_", " ").title())
            amount = abs(val)
            
            if val > 500: # Threshold for significance
                positives.append(f"Your **{label}** is a major strengths, adding approximately **${amount:,.0f}** to your baseline.")
            elif val < -500:
                negatives.append(f"Your **{label}** is currently weighing down your estimate by about **${amount:,.0f}**.")

        # Headline
        if pred_val > base_val:
            headline = "Good news! You're trending above the global market average."
        else:
            headline = "Your profile is currently leaning below the global average for this role."

        return {
            "headline": headline,
            "base_salary": round(base_val, 2),
            "predicted_salary": round(pred_val, 2),
            "positives": positives[:3], # Top 3
            "negatives": negatives[:2], # Top 2
            "summary": f"In summary, the model sees your {list(contributions.keys())[0].replace('_',' ')} as the primary driver of your compensation value."
        }
        
    except Exception as e:
        logger.error(f"Story generation failed: {e}")
        return {"error": str(e)}

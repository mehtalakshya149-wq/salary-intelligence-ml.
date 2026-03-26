"""
resume_parser.py -- Resume-to-Salary Estimation
=================================================
Extracts profile features from resume text using rule-based
keyword matching, then maps them to a salary prediction.

NLP Architecture (rule-based, no heavy NLP dependencies):

    Resume Text
        |
        v
    [Keyword Extraction]
        - Regex + predefined skill/role/level dictionaries
        - Case-insensitive, word-boundary aware matching
        |
        v
    [Entity Mapping]
        - Map extracted keywords to model input features:
          job_title, experience_level, skills, etc.
        - Use frequency and context signals for confidence
        |
        v
    [Profile Assembly]
        - Fill missing fields with sensible defaults
        - Validate against expected schema
        |
        v
    [Salary Prediction]
        - Call predict.run_prediction() with assembled profile
        |
        v
    {estimated_salary, extracted_features, confidence, explanation}

Future Enhancement (ML-based NLP):
    - spaCy NER for entity extraction
    - Sentence-BERT for semantic skill matching
    - HuggingFace transformers for resume section classification
    - These would improve accuracy but add heavy dependencies
"""

import re
import logging
from typing import Any

from ml.src.preprocess import load_config
from ml.src.predict import run_prediction

logger = logging.getLogger(__name__)


# -- Dictionaries -------------------------------------------

# Skills dictionary (lowercase)
SKILL_DICTIONARY = {
    # Programming
    "python", "r", "sql", "java", "scala", "julia", "c++", "go",
    "javascript", "typescript", "rust", "matlab", "sas", "stata",
    # ML/AI
    "tensorflow", "pytorch", "keras", "scikit-learn", "sklearn",
    "xgboost", "lightgbm", "catboost", "huggingface", "transformers",
    "opencv", "spacy", "nltk", "gensim",
    # Data
    "pandas", "numpy", "scipy", "matplotlib", "seaborn", "plotly",
    "spark", "pyspark", "hadoop", "hive", "kafka", "flink",
    "dbt", "airflow", "dagster", "prefect", "luigi",
    # Cloud/Infra
    "aws", "gcp", "azure", "docker", "kubernetes", "terraform",
    "mlflow", "kubeflow", "sagemaker", "vertex ai",
    # BI/Analytics
    "tableau", "power bi", "looker", "metabase", "excel",
    "snowflake", "redshift", "bigquery", "databricks", "dask",
    # Databases
    "postgresql", "mysql", "mongodb", "cassandra", "redis",
    "elasticsearch", "neo4j", "dynamodb",
}

# Role keyword mappings (keyword -> job_title)
ROLE_KEYWORDS = {
    "data scientist": "Data Scientist",
    "data science": "Data Scientist",
    "machine learning engineer": "ML Engineer",
    "ml engineer": "ML Engineer",
    "mlops": "MLOps Engineer",
    "data engineer": "Data Engineer",
    "data analyst": "Data Analyst",
    "business analyst": "Business Analyst",
    "analytics engineer": "Analytics Engineer",
    "bi analyst": "BI Analyst",
    "business intelligence": "BI Analyst",
    "research scientist": "Research Scientist",
    "data architect": "Data Architect",
    "nlp engineer": "NLP Engineer",
    "computer vision": "ML Engineer",
    "ai engineer": "ML Engineer",
    "head of data": "Head of Data",
    "director of data": "Head of Data",
    "chief data": "Head of Data",
}

# Experience level signals
EXPERIENCE_SIGNALS = {
    "ex": [
        "director", "vp", "vice president", "head of", "chief",
        "c-level", "cto", "cdo", "principal", "distinguished",
        "15+ years", "20+ years", "15 years", "20 years",
    ],
    "se": [
        "senior", "lead", "staff", "sr.", "sr ",
        "8+ years", "10+ years", "8 years", "10 years",
        "7+ years", "7 years", "9 years",
    ],
    "mi": [
        "mid-level", "mid level", "intermediate",
        "3+ years", "4+ years", "5+ years", "3 years",
        "4 years", "5 years", "6 years",
    ],
    "en": [
        "junior", "entry", "intern", "associate", "graduate",
        "fresher", "0-2 years", "1 year", "2 years",
        "entry-level", "entry level", "new grad",
    ],
}

# Employment type signals
EMPLOYMENT_SIGNALS = {
    "FT": ["full-time", "full time", "permanent", "fte"],
    "PT": ["part-time", "part time"],
    "CT": ["contract", "contractor", "consulting"],
    "FL": ["freelance", "freelancer", "self-employed"],
}


# -- Extraction Functions -----------------------------------

def extract_skills(text: str) -> list[str]:
    """
    Extract recognized skills from resume text.

    Uses word-boundary regex for each skill in the dictionary
    to avoid partial matches (e.g., 'R' inside 'Research').

    Args:
        text: Raw resume text.

    Returns:
        List of matched skill names.
    """
    text_lower = text.lower()
    found = []

    for skill in SKILL_DICTIONARY:
        # Use word boundaries for short terms, substring for longer
        if len(skill) <= 2:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                found.append(skill)
        else:
            if skill in text_lower:
                found.append(skill)

    # Deduplicate and sort
    found = sorted(set(found))
    logger.info(f"Extracted {len(found)} skills from resume")
    return found


def extract_experience_level(text: str) -> str:
    """
    Determine experience level from resume text.

    Checks for seniority signals from most senior to most junior,
    returning the first match. Defaults to 'MI' (mid-level).

    Args:
        text: Raw resume text.

    Returns:
        Experience level code: EN, MI, SE, or EX.
    """
    text_lower = text.lower()

    # Check from most senior to least
    for level in ["ex", "se", "mi", "en"]:
        for signal in EXPERIENCE_SIGNALS[level]:
            if signal in text_lower:
                logger.info(f"Experience level detected: {level.upper()} (signal: '{signal}')")
                return level.upper()

    logger.info("Experience level defaulting to MI")
    return "MI"


def extract_job_title(text: str) -> str:
    """
    Identify the most likely job title from resume text.

    Matches against predefined role keywords, preferring
    more specific titles (longer keyword matches).

    Args:
        text: Raw resume text.

    Returns:
        Best-match job title string.
    """
    text_lower = text.lower()
    matches = []

    for keyword, title in ROLE_KEYWORDS.items():
        if keyword in text_lower:
            matches.append((keyword, title))

    if matches:
        # Prefer longest keyword match (most specific)
        best = max(matches, key=lambda x: len(x[0]))
        logger.info(f"Job title detected: {best[1]} (keyword: '{best[0]}')")
        return best[1]

    logger.info("Job title defaulting to Data Scientist")
    return "Data Scientist"


def extract_employment_type(text: str) -> str:
    """
    Detect employment type from resume text.

    Args:
        text: Raw resume text.

    Returns:
        Employment type code: FT, PT, CT, or FL.
    """
    text_lower = text.lower()

    for emp_type, signals in EMPLOYMENT_SIGNALS.items():
        for signal in signals:
            if signal in text_lower:
                return emp_type

    return "FT"  # Default to full-time


def extract_years_of_experience(text: str) -> int | None:
    """
    Extract numeric years of experience from resume text.

    Looks for patterns like '5 years', '5+ years', '5-7 years'.

    Args:
        text: Raw resume text.

    Returns:
        Estimated years of experience, or None if not found.
    """
    patterns = [
        r'(\d{1,2})\+?\s*years?\s*(?:of\s+)?(?:experience|exp)',
        r'(\d{1,2})\+?\s*years?\s+in\s+(?:data|ml|ai|analytics)',
        r'experience\s*:\s*(\d{1,2})\+?\s*years?',
        r'(\d{1,2})\s*-\s*\d{1,2}\s*years?',
    ]

    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            years = int(match.group(1))
            logger.info(f"Years of experience detected: {years}")
            return years

    return None


# -- Profile Assembly ---------------------------------------

def build_profile_from_resume(
    text: str,
    config: dict | None = None,
) -> dict:
    """
    Assemble a prediction-ready profile from resume text.

    Extracts all available fields, fills missing ones with
    sensible defaults suitable for the prediction model.

    Args:
        text: Raw resume text.
        config: Optional parsed config dict.

    Returns:
        Dict matching the expected model input schema.
    """
    skills = extract_skills(text)
    experience_level = extract_experience_level(text)
    job_title = extract_job_title(text)
    employment_type = extract_employment_type(text)
    years_exp = extract_years_of_experience(text)

    profile = {
        "job_title": job_title,
        "experience_level": experience_level,
        "employment_type": employment_type,
        "company_location": "US",          # Default assumption
        "company_size": "M",               # Default assumption
        "remote_ratio": 50,                # Hybrid default
        "skills": ", ".join(skills) if skills else "Python, SQL",
        "work_year": 2026,                 # Current year
    }

    # Extraction metadata (not used by model, but useful for display)
    extraction_meta = {
        "skills_found": skills,
        "skills_count": len(skills),
        "experience_level_detected": experience_level,
        "job_title_detected": job_title,
        "employment_type_detected": employment_type,
        "years_of_experience": years_exp,
        "fields_defaulted": ["company_location", "company_size", "remote_ratio"],
    }

    return profile, extraction_meta


# -- End-to-End Estimation ----------------------------------

def estimate_salary_from_resume(
    text: str,
    config_path: str = "ml/config.yaml",
) -> dict:
    """
    Full resume-to-salary pipeline:
    1. Extract features from resume text
    2. Build prediction-ready profile
    3. Run salary prediction
    4. Return results with extraction explanation

    Args:
        text: Raw resume text (plain text, not PDF).
        config_path: Path to config YAML.

    Returns:
        Dict with salary estimate, extracted features, and explanation.
    """
    if not text or not text.strip():
        return {"error": "Empty resume text provided."}

    profile, extraction_meta = build_profile_from_resume(text)

    # Run prediction
    prediction = run_prediction(profile, config_path)

    return {
        "salary_estimate": prediction["salary"],
        "confidence": prediction["confidence"],
        "inflation_adjusted": prediction["inflation_adjusted"],
        "extracted_profile": profile,
        "extraction_details": extraction_meta,
        "explanation": _build_explanation(profile, extraction_meta),
    }


def _build_explanation(profile: dict, meta: dict) -> str:
    """Build a human-readable explanation of the estimation."""
    lines = [
        "Resume Analysis Summary:",
        f"  Role identified: {profile['job_title']}",
        f"  Experience level: {profile['experience_level']}",
        f"  Skills found: {meta['skills_count']} "
        f"({', '.join(meta['skills_found'][:5])}{'...' if meta['skills_count'] > 5 else ''})",
        f"  Employment type: {profile['employment_type']}",
    ]
    if meta["years_of_experience"]:
        lines.append(f"  Years of experience: {meta['years_of_experience']}")

    lines.append(f"\n  Defaulted fields: {', '.join(meta['fields_defaulted'])}")
    lines.append("  Note: For more accurate results, provide company location and size.")

    return "\n".join(lines)


# -- Architecture Documentation ----------------------------

def get_nlp_architecture_explanation() -> dict:
    """
    Return a structured explanation of the NLP pipeline design.

    This documents the current rule-based approach and the
    proposed ML-based enhancement path.

    Returns:
        Dict with architecture stages, rationale, and future plan.
    """
    return {
        "current_approach": {
            "name": "Rule-Based Keyword Extraction",
            "stages": [
                {
                    "stage": "1. Text Preprocessing",
                    "method": "Lowercasing, whitespace normalization",
                    "rationale": "Ensures case-insensitive matching",
                },
                {
                    "stage": "2. Skill Extraction",
                    "method": "Regex with word-boundary matching against a curated dictionary of 70+ skills",
                    "rationale": "High precision, no false positives from partial matches",
                },
                {
                    "stage": "3. Role Detection",
                    "method": "Longest-match keyword lookup against role dictionary",
                    "rationale": "Prefers specific roles (e.g., 'ML Engineer' over 'Engineer')",
                },
                {
                    "stage": "4. Experience Level Detection",
                    "method": "Priority-ordered signal matching (EX > SE > MI > EN)",
                    "rationale": "Catches seniority signals like 'senior', '10+ years'",
                },
                {
                    "stage": "5. Profile Assembly",
                    "method": "Map extracted entities to model input schema, fill defaults",
                    "rationale": "Ensures valid input for the salary prediction model",
                },
                {
                    "stage": "6. Salary Prediction",
                    "method": "Feed assembled profile to trained RF+GB ensemble",
                    "rationale": "Reuses the validated prediction pipeline for consistency",
                },
            ],
            "strengths": [
                "Zero additional dependencies",
                "Fully explainable -- every extraction step is traceable",
                "Fast execution (no model loading for NLP)",
                "Easy to extend skill/role dictionaries",
            ],
            "limitations": [
                "Cannot understand context (e.g., 'managed a team of data scientists')",
                "Misses skills not in the dictionary",
                "No semantic similarity matching",
            ],
        },
        "future_ml_approach": {
            "name": "ML-Based NLP Pipeline (Proposed Enhancement)",
            "components": [
                {
                    "component": "spaCy NER",
                    "purpose": "Named Entity Recognition for skill, role, and company extraction",
                    "dependency": "spacy + en_core_web_sm",
                },
                {
                    "component": "Sentence-BERT",
                    "purpose": "Semantic skill matching (handle synonyms and variations)",
                    "dependency": "sentence-transformers",
                },
                {
                    "component": "Resume Section Classifier",
                    "purpose": "Classify resume sections (Education, Experience, Skills)",
                    "dependency": "transformers (HuggingFace)",
                },
                {
                    "component": "PDF/DOCX Parser",
                    "purpose": "Extract text from uploaded resume files",
                    "dependency": "pdfplumber, python-docx",
                },
            ],
        },
    }

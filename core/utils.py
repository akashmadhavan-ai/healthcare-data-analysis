# core/utils.py
# Helper functions used across
# all modules in the project

import pandas as pd
import numpy as np
import os
import hashlib
from datetime import datetime

# ─────────────────────────────────────────
# SECTION 1 — Column Type Detection
# ─────────────────────────────────────────

def get_numeric_columns(df):
    """
    Return list of numeric column names
    Works with any dataset automatically
    """
    return df.select_dtypes(
        include=["float64", "int64",
                 "float32", "int32"]
    ).columns.tolist()


def get_categorical_columns(df):
    """
    Return list of categorical column names
    """
    return df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()


def get_datetime_columns(df):
    """
    Return list of datetime column names
    Also tries to detect date strings
    """
    datetime_cols = df.select_dtypes(
        include=["datetime64"]
    ).columns.tolist()

    # Try detecting date strings
    for col in get_categorical_columns(df):
        try:
            pd.to_datetime(
                df[col].dropna().head(10)
            )
            datetime_cols.append(col)
        except:
            pass

    return datetime_cols


def get_binary_columns(df):
    """
    Return columns that have only 2 values
    Useful for finding target columns
    """
    binary_cols = []
    for col in df.columns:
        if df[col].nunique() == 2:
            binary_cols.append(col)
    return binary_cols


def detect_column_type(df, col):
    """
    Detect the semantic type of a column
    Returns one of:
    'numeric', 'categorical',
    'binary', 'datetime', 'id', 'text'
    """
    # Check datetime first
    if df[col].dtype == "datetime64[ns]":
        return "datetime"

    # Check numeric
    if df[col].dtype in [
        "float64", "int64",
        "float32", "int32"
    ]:
        # Check if it's an ID column
        if df[col].nunique() == len(df):
            return "id"

        # Check if binary
        if df[col].nunique() == 2:
            return "binary"

        return "numeric"

    # Check object columns
    if df[col].dtype == "object":
        # Try datetime parse
        try:
            pd.to_datetime(
                df[col].dropna().head(5)
            )
            return "datetime"
        except:
            pass

        # Check cardinality
        cardinality = df[col].nunique()
        total = len(df)

        # High cardinality = text or ID
        if cardinality / total > 0.9:
            return "id"

        # Low cardinality = categorical
        return "categorical"

    return "unknown"


# ─────────────────────────────────────────
# SECTION 2 — Dataset Quality Checks
# ─────────────────────────────────────────

def calculate_quality_score(df):
    """
    Calculate data quality score 0-100
    Based on:
    - Completeness (missing values)
    - Uniqueness (duplicates)
    - Consistency (data types)
    """
    scores = {}
    total_cells = df.shape[0] * df.shape[1]

    # Completeness score
    missing = df.isna().sum().sum()
    completeness = max(
        0,
        100 - (missing / total_cells * 100)
    )
    scores["completeness"] = round(
        completeness, 1
    )

    # Uniqueness score
    duplicates = df.duplicated().sum()
    uniqueness = max(
        0,
        100 - (duplicates / len(df) * 100)
    )
    scores["uniqueness"] = round(uniqueness, 1)

    # Consistency score
    # Check if numeric columns have
    # unexpected string values
    inconsistent = 0
    for col in df.columns:
        if df[col].dtype == "object":
            try:
                pd.to_numeric(df[col])
                inconsistent += 1
            except:
                pass

    consistency = max(
        0,
        100 - (
            inconsistent /
            len(df.columns) * 100
        )
    )
    scores["consistency"] = round(
        consistency, 1
    )

    # Overall score (weighted average)
    overall = (
        scores["completeness"] * 0.5 +
        scores["uniqueness"] * 0.3 +
        scores["consistency"] * 0.2
    )
    scores["overall"] = round(overall, 1)

    return scores


def get_quality_label(score):
    """
    Convert quality score to label
    """
    if score >= 90:
        return "Excellent", "🟢"
    elif score >= 75:
        return "Good", "🟡"
    elif score >= 60:
        return "Fair", "🟠"
    else:
        return "Poor", "🔴"


def get_missing_summary(df):
    """
    Detailed missing value summary
    per column
    """
    missing_data = []

    for col in df.columns:
        missing_count = df[col].isna().sum()
        if missing_count > 0:
            missing_data.append({
                "column": col,
                "missing_count": int(
                    missing_count
                ),
                "missing_pct": round(
                    missing_count /
                    len(df) * 100, 1
                ),
                "dtype": str(df[col].dtype)
            })

    if not missing_data:
        return pd.DataFrame()

    return pd.DataFrame(missing_data)\
        .sort_values(
            "missing_pct",
            ascending=False
        )


# ─────────────────────────────────────────
# SECTION 3 — Statistical Helpers
# ─────────────────────────────────────────

def detect_outliers_iqr(series):
    """
    Detect outliers using IQR method
    Returns dict with outlier info
    """
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = series[
        (series < lower_bound) |
        (series > upper_bound)
    ]

    return {
        "count": len(outliers),
        "percentage": round(
            len(outliers) /
            len(series) * 100, 1
        ),
        "lower_bound": round(lower_bound, 2),
        "upper_bound": round(upper_bound, 2),
        "outlier_values": outliers.tolist()
    }


def calculate_skewness_label(skewness):
    """
    Convert skewness value to readable label
    """
    if abs(skewness) < 0.5:
        return "Symmetric", "normal"
    elif abs(skewness) < 1.0:
        direction = "right" if skewness > 0 \
            else "left"
        return f"Moderately {direction} skewed", \
               "warning"
    else:
        direction = "right" if skewness > 0 \
            else "left"
        return f"Highly {direction} skewed", \
               "error"


def get_correlation_label(corr_value):
    """
    Convert correlation value to label
    """
    abs_corr = abs(corr_value)
    direction = "positive" if corr_value > 0 \
        else "negative"

    if abs_corr >= 0.8:
        return f"Very strong {direction}"
    elif abs_corr >= 0.6:
        return f"Strong {direction}"
    elif abs_corr >= 0.4:
        return f"Moderate {direction}"
    elif abs_corr >= 0.2:
        return f"Weak {direction}"
    else:
        return "Very weak / no correlation"


def get_top_correlations(df, target_col=None,
                          threshold=0.3):
    """
    Get top correlated column pairs
    above threshold
    """
    numeric_cols = get_numeric_columns(df)
    if len(numeric_cols) < 2:
        return []

    corr_matrix = df[numeric_cols].corr()
    correlations = []

    for i in range(len(corr_matrix.columns)):
        for j in range(
            i + 1, len(corr_matrix.columns)
        ):
            col1 = corr_matrix.columns[i]
            col2 = corr_matrix.columns[j]
            val = corr_matrix.iloc[i, j]

            if abs(val) >= threshold:
                correlations.append({
                    "column_1": col1,
                    "column_2": col2,
                    "correlation": round(val, 3),
                    "abs_correlation": round(
                        abs(val), 3
                    ),
                    "label": get_correlation_label(
                        val
                    )
                })

    return sorted(
        correlations,
        key=lambda x: x["abs_correlation"],
        reverse=True
    )


# ─────────────────────────────────────────
# SECTION 4 — Formatting Helpers
# ─────────────────────────────────────────

def format_number(value):
    """
    Format large numbers readably
    1000 → 1K, 1000000 → 1M
    """
    try:
        value = float(value)
        if value >= 1_000_000:
            return f"{value/1_000_000:.1f}M"
        elif value >= 1_000:
            return f"{value/1_000:.1f}K"
        elif value == int(value):
            return str(int(value))
        else:
            return f"{value:.2f}"
    except:
        return str(value)


def format_percentage(value, decimals=1):
    """Format value as percentage"""
    try:
        return f"{float(value):.{decimals}f}%"
    except:
        return "N/A"


def truncate_text(text, max_length=50):
    """Truncate long text with ellipsis"""
    if len(str(text)) > max_length:
        return str(text)[:max_length] + "..."
    return str(text)


def get_column_display_name(col_name):
    """
    Convert column names to readable format
    glucose_level → Glucose Level
    BMI → BMI
    blood_pressure → Blood Pressure
    """
    # Handle all-caps acronyms
    if col_name.isupper():
        return col_name

    # Replace underscores with spaces
    # and title case
    return col_name.replace(
        "_", " "
    ).title()


# ─────────────────────────────────────────
# SECTION 5 — File Helpers
# ─────────────────────────────────────────

def get_file_size(file):
    """
    Get file size in human readable format
    """
    try:
        size = file.size
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size/1024:.1f} KB"
        else:
            return f"{size/(1024*1024):.1f} MB"
    except:
        return "Unknown"


def get_file_hash(file):
    """
    Generate unique hash for uploaded file
    Used to detect same file re-uploaded
    """
    try:
        content = file.read()
        file.seek(0)  # reset pointer
        return hashlib.md5(
            content
        ).hexdigest()[:8]
    except:
        return "unknown"


def validate_csv_file(df):
    """
    Validate uploaded CSV is usable
    Returns (is_valid, error_message)
    """
    # Check not empty
    if df is None or len(df) == 0:
        return False, \
            "File is empty. Please upload a " \
            "file with data."

    # Check has enough rows
    if len(df) < 5:
        return False, \
            f"File only has {len(df)} rows. " \
            f"Need at least 5 rows for analysis."

    # Check has enough columns
    if len(df.columns) < 2:
        return False, \
            "File only has 1 column. " \
            "Need at least 2 columns."

    # Check has numeric data
    numeric_cols = get_numeric_columns(df)
    if len(numeric_cols) == 0:
        return False, \
            "No numeric columns found. " \
            "Analysis requires numeric data."

    return True, "File is valid"


# ─────────────────────────────────────────
# SECTION 6 — Domain Detection
# ─────────────────────────────────────────

def detect_dataset_domain(df):
    """
    Auto detect what kind of dataset
    was uploaded based on column names

    Returns: domain name and confidence
    """
    columns_lower = [
        col.lower() for col in df.columns
    ]
    col_string = " ".join(columns_lower)

    # Domain keyword mapping
    domain_keywords = {
        "healthcare": [
            "glucose", "insulin", "bmi",
            "blood", "pressure", "patient",
            "diagnosis", "outcome", "age",
            "diabetes", "cholesterol",
            "heart", "cancer", "clinical"
        ],
        "sales": [
            "revenue", "sales", "product",
            "order", "customer", "price",
            "quantity", "transaction",
            "category", "profit", "discount"
        ],
        "workflow": [
            "task", "status", "assignee",
            "deadline", "priority", "sprint",
            "delay", "completion", "cycle",
            "workflow", "ticket", "issue"
        ],
        "finance": [
            "stock", "price", "volume",
            "market", "trade", "portfolio",
            "return", "risk", "asset"
        ],
        "hr": [
            "employee", "salary", "department",
            "hire", "performance", "attrition",
            "tenure", "position", "manager"
        ]
    }

    scores = {}
    for domain, keywords in \
            domain_keywords.items():
        score = sum(
            1 for keyword in keywords
            if keyword in col_string
        )
        scores[domain] = score

    # Get best match
    best_domain = max(
        scores, key=scores.get
    )
    best_score = scores[best_domain]

    if best_score == 0:
        return "general", 0.0

    # Calculate confidence
    confidence = min(
        1.0, best_score /
        len(domain_keywords[best_domain])
    )

    return best_domain, round(confidence, 2)


def get_domain_icon(domain):
    """Return emoji icon for domain"""
    icons = {
        "healthcare": "🏥",
        "sales":      "📈",
        "workflow":   "⚙️",
        "finance":    "💰",
        "hr":         "👥",
        "general":    "📊"
    }
    return icons.get(domain, "📊")


# ─────────────────────────────────────────
# SECTION 7 — Session & Cache Helpers
# ─────────────────────────────────────────

def generate_session_id():
    """Generate unique session identifier"""
    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )
    return f"session_{timestamp}"


def get_timestamp():
    """Get formatted current timestamp"""
    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


def safe_divide(numerator,
                denominator,
                default=0):
    """Safe division avoiding zero error"""
    try:
        if denominator == 0:
            return default
        return numerator / denominator
    except:
        return default

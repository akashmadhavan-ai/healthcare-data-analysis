# core/utils.py

import os
import hashlib
from datetime import datetime

import numpy as np
import pandas as pd


# ─────────────────────────────────────────
# SECTION 1 — COLUMN DETECTION
# ─────────────────────────────────────────

def get_numeric_columns(df):

    """
    Return numeric columns
    """

    return (
        df.select_dtypes(
            include=[
                "int64",
                "float64",
                "int32",
                "float32"
            ]
        )
        .columns
        .tolist()
    )


def get_categorical_columns(df):

    """
    Return categorical columns
    """

    return (
        df.select_dtypes(
            include=[
                "object",
                "category",
                "bool"
            ]
        )
        .columns
        .tolist()
    )


def get_datetime_columns(df):

    """
    Return datetime columns
    """

    datetime_cols = (
        df.select_dtypes(
            include=["datetime64"]
        )
        .columns
        .tolist()
    )

    for col in get_categorical_columns(df):

        try:

            pd.to_datetime(
                df[col]
                .dropna()
                .head(10)
            )

            datetime_cols.append(col)

        except Exception:

            continue

    return list(set(datetime_cols))


def get_binary_columns(df):

    """
    Return binary columns
    """

    binary_cols = []

    for col in df.columns:

        unique_vals = (
            df[col]
            .dropna()
            .unique()
        )

        if len(unique_vals) == 2:

            binary_cols.append(col)

    return binary_cols


def detect_column_type(df, col):

    """
    Detect semantic column type
    """

    if col not in df.columns:

        return "unknown"

    series = df[col]

    # Datetime

    if pd.api.types.is_datetime64_any_dtype(
        series
    ):

        return "datetime"

    # Numeric

    if pd.api.types.is_numeric_dtype(
        series
    ):

        if series.nunique() == len(series):

            return "id"

        if series.nunique() == 2:

            return "binary"

        return "numeric"

    # Object

    if pd.api.types.is_object_dtype(
        series
    ):

        try:

            pd.to_datetime(
                series.dropna().head(5)
            )

            return "datetime"

        except Exception:

            pass

        cardinality = (
            series.nunique() /
            max(len(series), 1)
        )

        if cardinality > 0.9:

            return "id"

        return "categorical"

    return "unknown"


# ─────────────────────────────────────────
# SECTION 2 — QUALITY HELPERS
# ─────────────────────────────────────────

def calculate_quality_score(df):

    """
    Calculate dataset quality score
    """

    if df.empty:

        return {

            "completeness": 0,
            "uniqueness": 0,
            "consistency": 0,
            "overall": 0
        }

    total_cells = (
        df.shape[0] *
        df.shape[1]
    )

    # Missing values

    missing = (
        df.isna()
        .sum()
        .sum()
    )

    completeness = max(

        0,

        100 - (
            missing /
            total_cells * 100
        )
    )

    # Duplicates

    duplicates = (
        df.duplicated()
        .sum()
    )

    uniqueness = max(

        0,

        100 - (
            duplicates /
            len(df) * 100
        )
    )

    # Consistency

    inconsistent = 0

    for col in df.columns:

        if df[col].dtype == "object":

            try:

                pd.to_numeric(df[col])

                inconsistent += 1

            except Exception:

                continue

    consistency = max(

        0,

        100 - (
            inconsistent /
            len(df.columns) * 100
        )
    )

    overall = (

        completeness * 0.5 +

        uniqueness * 0.3 +

        consistency * 0.2
    )

    return {

        "completeness":
            round(completeness, 1),

        "uniqueness":
            round(uniqueness, 1),

        "consistency":
            round(consistency, 1),

        "overall":
            round(overall, 1)
    }


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

    return "Poor", "🔴"


def get_missing_summary(df):

    """
    Return missing value summary
    """

    missing_data = []

    for col in df.columns:

        missing_count = (
            df[col]
            .isna()
            .sum()
        )

        if missing_count > 0:

            missing_data.append({

                "column":
                    col,

                "missing_count":
                    int(missing_count),

                "missing_pct":
                    round(
                        (
                            missing_count /
                            len(df)
                        ) * 100,
                        2
                    ),

                "dtype":
                    str(df[col].dtype)
            })

    if not missing_data:

        return pd.DataFrame()

    return (

        pd.DataFrame(missing_data)

        .sort_values(
            by="missing_pct",
            ascending=False
        )
    )


# ─────────────────────────────────────────
# SECTION 3 — STATISTICAL HELPERS
# ─────────────────────────────────────────

def detect_outliers_iqr(series):

    """
    Detect outliers using IQR
    """

    Q1 = series.quantile(0.25)

    Q3 = series.quantile(0.75)

    IQR = Q3 - Q1

    lower_bound = (
        Q1 - 1.5 * IQR
    )

    upper_bound = (
        Q3 + 1.5 * IQR
    )

    outliers = series[
        (
            series < lower_bound
        ) |
        (
            series > upper_bound
        )
    ]

    return {

        "count":
            len(outliers),

        "percentage":
            round(
                (
                    len(outliers) /
                    len(series)
                ) * 100,
                2
            ),

        "lower_bound":
            round(lower_bound, 2),

        "upper_bound":
            round(upper_bound, 2),

        "outlier_values":
            outliers.tolist()
    }


def calculate_skewness_label(skewness):

    """
    Convert skewness to label
    """

    if abs(skewness) < 0.5:

        return "Symmetric", "normal"

    elif abs(skewness) < 1.0:

        direction = (
            "right"
            if skewness > 0
            else "left"
        )

        return (
            f"Moderately "
            f"{direction} skewed",
            "warning"
        )

    direction = (
        "right"
        if skewness > 0
        else "left"
    )

    return (

        f"Highly "
        f"{direction} skewed",

        "error"
    )


def get_correlation_label(corr_value):

    """
    Convert correlation value to label
    """

    abs_corr = abs(corr_value)

    direction = (
        "positive"
        if corr_value > 0
        else "negative"
    )

    if abs_corr >= 0.8:

        return f"Very strong {direction}"

    elif abs_corr >= 0.6:

        return f"Strong {direction}"

    elif abs_corr >= 0.4:

        return f"Moderate {direction}"

    elif abs_corr >= 0.2:

        return f"Weak {direction}"

    return "Very weak / no correlation"


def get_top_correlations(
    df,
    threshold=0.3
):

    """
    Return top correlations
    """

    numeric_cols = get_numeric_columns(df)

    if len(numeric_cols) < 2:

        return []

    corr_matrix = (
        df[numeric_cols]
        .corr()
        .fillna(0)
    )

    correlations = []

    for i in range(
        len(corr_matrix.columns)
    ):

        for j in range(
            i + 1,
            len(corr_matrix.columns)
        ):

            col1 = corr_matrix.columns[i]

            col2 = corr_matrix.columns[j]

            value = corr_matrix.iloc[i, j]

            if abs(value) >= threshold:

                correlations.append({

                    "column_1":
                        col1,

                    "column_2":
                        col2,

                    "correlation":
                        round(value, 3),

                    "abs_correlation":
                        round(abs(value), 3),

                    "label":
                        get_correlation_label(
                            value
                        )
                })

    return sorted(

        correlations,

        key=lambda x:
        x["abs_correlation"],

        reverse=True
    )


# ─────────────────────────────────────────
# SECTION 4 — FORMATTING HELPERS
# ─────────────────────────────────────────

def format_number(value):

    """
    Format numbers nicely
    """

    try:

        value = float(value)

        if value >= 1_000_000:

            return (
                f"{value/1_000_000:.1f}M"
            )

        elif value >= 1_000:

            return (
                f"{value/1_000:.1f}K"
            )

        elif value == int(value):

            return str(int(value))

        return f"{value:.2f}"

    except Exception:

        return str(value)


def format_percentage(
    value,
    decimals=1
):

    """
    Format percentage
    """

    try:

        return (
            f"{float(value):.{decimals}f}%"
        )

    except Exception:

        return "N/A"


def truncate_text(
    text,
    max_length=50
):

    """
    Truncate long text
    """

    text = str(text)

    if len(text) > max_length:

        return (
            text[:max_length] + "..."
        )

    return text


def get_column_display_name(col_name):

    """
    Format column name nicely
    """

    if str(col_name).isupper():

        return str(col_name)

    return (
        str(col_name)
        .replace("_", " ")
        .title()
    )


# ─────────────────────────────────────────
# SECTION 5 — FILE HELPERS
# ─────────────────────────────────────────

def get_file_size(file):

    """
    Get readable file size
    """

    try:

        size = file.size

        if size < 1024:

            return f"{size} B"

        elif size < 1024 * 1024:

            return (
                f"{size / 1024:.1f} KB"
            )

        return (
            f"{size / (1024*1024):.1f} MB"
        )

    except Exception:

        return "Unknown"


def get_file_hash(file):

    """
    Generate file hash
    """

    try:

        content = file.read()

        file.seek(0)

        return hashlib.md5(
            content
        ).hexdigest()[:8]

    except Exception:

        return "unknown"


def validate_csv_file(df):

    """
    Validate uploaded CSV
    """

    if df is None or df.empty:

        return (
            False,
            "Dataset is empty"
        )

    if len(df) < 5:

        return (
            False,
            (
                "Dataset must contain "
                "at least 5 rows"
            )
        )

    if len(df.columns) < 2:

        return (
            False,
            (
                "Dataset must contain "
                "at least 2 columns"
            )
        )

    numeric_cols = (
        get_numeric_columns(df)
    )

    if len(numeric_cols) == 0:

        return (
            False,
            (
                "No numeric columns found"
            )
        )

    return True, "Dataset is valid"


# ─────────────────────────────────────────
# SECTION 6 — SESSION HELPERS
# ─────────────────────────────────────────

def generate_session_id():

    """
    Generate session ID
    """

    timestamp = (
        datetime.now()
        .strftime(
            "%Y%m%d_%H%M%S"
        )
    )

    return f"session_{timestamp}"


def get_timestamp():

    """
    Return current timestamp
    """

    return (
        datetime.now()
        .strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )


def safe_divide(
    numerator,
    denominator,
    default=0
):

    """
    Safe division
    """

    try:

        if denominator == 0:

            return default

        return (
            numerator /
            denominator
        )

    except Exception:

        return default
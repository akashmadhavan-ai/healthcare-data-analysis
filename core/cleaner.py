# core/cleaner.py

import pandas as pd
import numpy as np


class DataCleaner:

    def __init__(self):

        self.report = []

        self.original_shape = None
        self.cleaned_shape = None

        self.removed_duplicates = 0
        self.fixed_datatypes = []
        self.filled_missing = {}
        self.invalid_values_fixed = {}
        self.outliers_detected = {}

    # ─────────────────────────────────────
    # MAIN CLEANING PIPELINE
    # ─────────────────────────────────────

    def clean(self, df):

        if df.empty:
            raise ValueError(
                "Input dataset is empty"
            )

        df = df.copy()

        self.original_shape = df.shape

        self.report = []

        self.report.append(
            "🚀 Starting dataset cleaning pipeline"
        )

        df = self._remove_duplicates(df)

        df = self._fix_datatypes(df)

        df = self._handle_missing_values(df)

        df = self._remove_invalid_values(df)

        df = self._detect_outliers(df)

        self.cleaned_shape = df.shape

        self.report.append(
            (
                f"✅ Final dataset: "
                f"{self.cleaned_shape[0]} rows, "
                f"{self.cleaned_shape[1]} columns"
            )
        )

        return df

    # ─────────────────────────────────────
    # REMOVE DUPLICATES
    # ─────────────────────────────────────

    def _remove_duplicates(self, df):

        before = len(df)

        df = df.drop_duplicates()

        removed = before - len(df)

        self.removed_duplicates = removed

        if removed > 0:

            self.report.append(
                (
                    f"🗑️ Removed "
                    f"{removed} duplicate rows"
                )
            )

        else:

            self.report.append(
                "✅ No duplicate rows found"
            )

        return df

    # ─────────────────────────────────────
    # FIX DATATYPES
    # ─────────────────────────────────────

    def _fix_datatypes(self, df):

        fixed = []

        for col in df.columns:

            if df[col].dtype == "object":

                try:

                    converted = pd.to_numeric(
                        df[col],
                        errors="raise"
                    )

                    df[col] = converted

                    fixed.append(col)

                except Exception:
                    continue

        self.fixed_datatypes = fixed

        if fixed:

            self.report.append(
                (
                    "🔧 Fixed datatypes for: "
                    f"{', '.join(fixed)}"
                )
            )

        else:

            self.report.append(
                "✅ No datatype fixes needed"
            )

        return df

    # ─────────────────────────────────────
    # HANDLE MISSING VALUES
    # ─────────────────────────────────────

    def _handle_missing_values(self, df):

        for col in df.columns:

            missing = (
                df[col]
                .isna()
                .sum()
            )

            if missing > 0:

                if pd.api.types.is_numeric_dtype(
                    df[col]
                ):

                    median_val = (
                        df[col]
                        .median()
                    )

                    df[col] = df[col].fillna(
                        median_val
                    )

                    self.filled_missing[col] = {
                        "count": int(missing),
                        "method": "median",
                        "value": round(
                            float(median_val),
                            2
                        )
                    }

                    self.report.append(
                        (
                            f"📊 '{col}': "
                            f"filled {missing} "
                            f"missing values "
                            f"with median "
                            f"({median_val:.2f})"
                        )
                    )

                else:

                    mode_series = (
                        df[col]
                        .mode()
                    )

                    if len(mode_series) > 0:

                        mode_val = mode_series[0]

                    else:

                        mode_val = "Unknown"

                    df[col] = df[col].fillna(
                        mode_val
                    )

                    self.filled_missing[col] = {
                        "count": int(missing),
                        "method": "mode",
                        "value": str(mode_val)
                    }

                    self.report.append(
                        (
                            f"📝 '{col}': "
                            f"filled {missing} "
                            f"missing values "
                            f"with mode "
                            f"({mode_val})"
                        )
                    )

        return df

    # ─────────────────────────────────────
    # REMOVE INVALID VALUES
    # ─────────────────────────────────────

    def _remove_invalid_values(self, df):

        suspicious_keywords = [

            "glucose",
            "blood",
            "bmi",
            "insulin",
            "pressure",
            "skin",
            "cholesterol",
            "heart"

        ]

        suspicious_cols = [

            col for col in df.columns

            if any(
                keyword in col.lower()
                for keyword
                in suspicious_keywords
            )
        ]

        for col in suspicious_cols:

            if col in df.columns:

                if pd.api.types.is_numeric_dtype(
                    df[col]
                ):

                    zero_count = (
                        (df[col] == 0)
                        .sum()
                    )

                    if zero_count > 0:

                        median_val = (
                            df[col]
                            .replace(0, np.nan)
                            .median()
                        )

                        df[col] = (
                            df[col]
                            .replace(
                                0,
                                median_val
                            )
                        )

                        self.invalid_values_fixed[
                            col
                        ] = {
                            "count":
                                int(zero_count),

                            "replacement":
                                round(
                                    float(median_val),
                                    2
                                )
                        }

                        self.report.append(
                            (
                                f"⚠️ '{col}': "
                                f"replaced "
                                f"{zero_count} "
                                f"invalid zero values "
                                f"with median"
                            )
                        )

        return df

    # ─────────────────────────────────────
    # OUTLIER DETECTION
    # ─────────────────────────────────────

    def _detect_outliers(self, df):

        numeric_cols = (
            df.select_dtypes(
                include=[
                    "int64",
                    "float64",
                    "int32",
                    "float32"
                ]
            )
            .columns
        )

        for col in numeric_cols:

            Q1 = (
                df[col]
                .quantile(0.25)
            )

            Q3 = (
                df[col]
                .quantile(0.75)
            )

            IQR = Q3 - Q1

            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR

            outliers = df[
                (
                    df[col] < lower
                ) |
                (
                    df[col] > upper
                )
            ]

            count = len(outliers)

            if count > 0:

                self.outliers_detected[
                    col
                ] = {

                    "count":
                        count,

                    "percentage":
                        round(
                            (
                                count /
                                len(df)
                            ) * 100,
                            2
                        ),

                    "lower_bound":
                        round(lower, 2),

                    "upper_bound":
                        round(upper, 2)
                }

                self.report.append(
                    (
                        f"📈 '{col}': "
                        f"detected "
                        f"{count} outliers"
                    )
                )

        return df

    # ─────────────────────────────────────
    # CLEANING REPORT
    # ─────────────────────────────────────

    def get_report(self):

        return self.report

    # ─────────────────────────────────────
    # QUALITY SCORE
    # ─────────────────────────────────────

    def get_quality_score(
        self,
        df_original
    ):

        if df_original.empty:

            return 0

        issues = 0

        total_cells = (
            df_original.shape[0]
            * df_original.shape[1]
        )

        missing = (
            df_original
            .isna()
            .sum()
            .sum()
        )

        issues += missing

        duplicates = (
            df_original
            .duplicated()
            .sum()
        )

        issues += duplicates * 10

        score = max(

            0,

            100 - (
                (
                    issues /
                    total_cells
                ) * 100
            )
        )

        return round(score, 1)

    # ─────────────────────────────────────
    # CLEANING SUMMARY
    # ─────────────────────────────────────

    def get_cleaning_summary(self):

        return {

            "original_shape":
                self.original_shape,

            "cleaned_shape":
                self.cleaned_shape,

            "duplicates_removed":
                self.removed_duplicates,

            "datatype_fixes":
                self.fixed_datatypes,

            "missing_values_fixed":
                self.filled_missing,

            "invalid_values_fixed":
                self.invalid_values_fixed,

            "outliers_detected":
                self.outliers_detected,

            "report":
                self.report
        }

    # ─────────────────────────────────────
    # DATA PREVIEW
    # ─────────────────────────────────────

    def preview_cleaned_data(
        self,
        df,
        rows=5
    ):

        return df.head(rows)
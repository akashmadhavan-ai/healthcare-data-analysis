import pandas as pd
import numpy as np

class DataCleaner:
    def __init__(self):
        self.report = []
        self.original_shape = None
        self.cleaned_shape = None

    def clean(self, df):
        df = df.copy()
        self.original_shape = df.shape
        self.report = []

        df = self._remove_duplicates(df)
        df = self._fix_datatypes(df)
        df = self._handle_missing_values(df)
        df = self._remove_invalid_values(df)

        self.cleaned_shape = df.shape
        self.report.append(
            f"✅ Final dataset: "
            f"{self.cleaned_shape[0]} rows, "
            f"{self.cleaned_shape[1]} columns"
        )
        return df

    def _remove_duplicates(self, df):
        before = len(df)
        df = df.drop_duplicates()
        removed = before - len(df)
        if removed > 0:
            self.report.append(
                f"🗑️ Removed {removed} "
                f"duplicate rows"
            )
        else:
            self.report.append(
                f"✅ No duplicate rows found"
            )
        return df

    def _fix_datatypes(self, df):
        fixed = []
        for col in df.columns:
            # Try converting object columns
            # to numeric where possible
            if df[col].dtype == "object":
                try:
                    df[col] = pd.to_numeric(
                        df[col],
                        errors="ignore"
                    )
                    fixed.append(col)
                except:
                    pass
        if fixed:
            self.report.append(
                f"🔧 Fixed datatypes for: "
                f"{', '.join(fixed)}"
            )
        return df

    def _handle_missing_values(self, df):
        for col in df.columns:
            missing = df[col].isna().sum()
            if missing > 0:
                if df[col].dtype in [
                    "float64", "int64"
                ]:
                    # Numeric: fill with median
                    median_val = df[col].median()
                    df[col] = df[col].fillna(
                        median_val
                    )
                    self.report.append(
                        f"📊 '{col}': filled "
                        f"{missing} missing values "
                        f"with median "
                        f"({median_val:.2f})"
                    )
                else:
                    # Categorical: fill with mode
                    mode_val = df[col].mode()[0]
                    df[col] = df[col].fillna(
                        mode_val
                    )
                    self.report.append(
                        f"📝 '{col}': filled "
                        f"{missing} missing values "
                        f"with mode ({mode_val})"
                    )
        return df

    def _remove_invalid_values(self, df):
        # Auto detect columns where
        # zero is medically invalid
        suspicious_cols = [
            col for col in df.columns
            if any(keyword in col.lower()
                   for keyword in [
                       "glucose", "blood",
                       "bmi", "insulin",
                       "pressure", "skin"
                   ])
        ]
        for col in suspicious_cols:
            if col in df.columns:
                zero_count = (
                    df[col] == 0
                ).sum()
                if zero_count > 0:
                    df[col] = df[col].replace(
                        0, df[col].median()
                    )
                    self.report.append(
                        f"⚠️ '{col}': replaced "
                        f"{zero_count} invalid "
                        f"zero values with median"
                    )
        return df

    def get_report(self):
        return self.report

    def get_quality_score(self, df_original):
        """
        Score from 0-100
        Higher = cleaner original data
        """
        issues = 0
        total_cells = (
            df_original.shape[0] *
            df_original.shape[1]
        )

        # Missing values penalty
        missing = df_original.isna().sum().sum()
        issues += missing

        # Duplicate rows penalty
        dupes = df_original.duplicated().sum()
        issues += dupes * 10

        score = max(
            0,
            100 - (issues / total_cells * 100)
        )
        return round(score, 1)

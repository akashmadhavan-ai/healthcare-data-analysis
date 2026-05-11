# core/loader.py
# Handles all dataset loading,
# validation, and format detection

import pandas as pd
import numpy as np
import io
from core.utils import (
    validate_csv_file,
    detect_dataset_domain,
    get_domain_icon,
    get_file_size,
    get_file_hash,
    get_numeric_columns,
    get_categorical_columns,
    get_binary_columns,
    detect_column_type
)


class DataLoader:
    def __init__(self):
        self.raw_df = None
        self.file_info = {}
        self.load_errors = []
        self.load_warnings = []

    def load(self, uploaded_file):
        """
        Main load function
        Handles CSV files from Streamlit
        file uploader

        Returns:
        (dataframe, file_info, errors)
        """
        self.load_errors = []
        self.load_warnings = []

        try:
            # Step 1 — Get file info
            self.file_info = \
                self._extract_file_info(
                    uploaded_file
                )

            # Step 2 — Read CSV
            df = self._read_csv(uploaded_file)
            if df is None:
                return None, \
                    self.file_info, \
                    self.load_errors

            # Step 3 — Validate
            is_valid, error_msg = \
                validate_csv_file(df)
            if not is_valid:
                self.load_errors.append(
                    error_msg
                )
                return None, \
                    self.file_info, \
                    self.load_errors

            # Step 4 — Enrich file info
            self.file_info.update(
                self._build_dataset_info(df)
            )

            # Step 5 — Store and return
            self.raw_df = df
            return df, \
                self.file_info, \
                self.load_errors

        except Exception as e:
            self.load_errors.append(
                f"Failed to load file: {str(e)}"
            )
            return None, \
                self.file_info, \
                self.load_errors

    def _extract_file_info(self, file):
        """Extract metadata from file object"""
        return {
            "filename": file.name,
            "file_size": get_file_size(file),
            "file_hash": get_file_hash(file),
            "file_type": file.name.split(
                "."
            )[-1].upper()
        }

    def _read_csv(self, uploaded_file):
        """
        Read CSV with multiple encoding
        attempts — handles messy files
        """
        encodings = [
            "utf-8",
            "latin-1",
            "iso-8859-1",
            "cp1252"
        ]

        # Try different encodings
        for encoding in encodings:
            try:
                uploaded_file.seek(0)
                df = pd.read_csv(
                    uploaded_file,
                    encoding=encoding
                )
                self.load_warnings.append(
                    f"File read successfully "
                    f"({encoding} encoding)"
                ) if encoding != "utf-8" \
                    else None
                return df
            except UnicodeDecodeError:
                continue
            except pd.errors.EmptyDataError:
                self.load_errors.append(
                    "File is empty"
                )
                return None
            except pd.errors.ParserError as e:
                # Try with different separator
                try:
                    uploaded_file.seek(0)
                    df = pd.read_csv(
                        uploaded_file,
                        sep=";",
                        encoding=encoding
                    )
                    self.load_warnings.append(
                        "Detected semicolon "
                        "separator"
                    )
                    return df
                except:
                    continue

        self.load_errors.append(
            "Could not read file. "
            "Please ensure it is a valid CSV."
        )
        return None

    def _build_dataset_info(self, df):
        """
        Build comprehensive dataset
        information dictionary
        """
        # Detect domain
        domain, confidence = \
            detect_dataset_domain(df)

        # Column type breakdown
        numeric_cols = get_numeric_columns(df)
        categorical_cols = \
            get_categorical_columns(df)
        binary_cols = get_binary_columns(df)

        # Column type map
        col_types = {}
        for col in df.columns:
            col_types[col] = \
                detect_column_type(df, col)

        # Missing value summary
        total_cells = \
            df.shape[0] * df.shape[1]
        missing_count = \
            df.isna().sum().sum()
        missing_pct = round(
            missing_count /
            total_cells * 100, 1
        )

        # Duplicate summary
        duplicate_count = \
            df.duplicated().sum()

        return {
            "rows": len(df),
            "columns": len(df.columns),
            "numeric_columns": numeric_cols,
            "categorical_columns": \
                categorical_cols,
            "binary_columns": binary_cols,
            "column_types": col_types,
            "missing_count": int(
                missing_count
            ),
            "missing_pct": missing_pct,
            "duplicate_count": int(
                duplicate_count
            ),
            "domain": domain,
            "domain_confidence": confidence,
            "domain_icon": get_domain_icon(
                domain
            ),
            "column_names": df.columns\
                .tolist(),
            "memory_usage": f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB"
        }

    def get_sample(self, n=5):
        """Return first n rows"""
        if self.raw_df is not None:
            return self.raw_df.head(n)
        return None

    def get_column_summary(self):
        """
        Return per-column summary
        as DataFrame
        """
        if self.raw_df is None:
            return pd.DataFrame()

        summary = []
        for col in self.raw_df.columns:
            col_type = detect_column_type(
                self.raw_df, col
            )
            row = {
                "Column": col,
                "Type": col_type,
                "Missing": int(
                    self.raw_df[col]\
                        .isna().sum()
                ),
                "Missing %": round(
                    self.raw_df[col]\
                        .isna().sum() /
                    len(self.raw_df) * 100, 1
                ),
                "Unique Values": int(
                    self.raw_df[col].nunique()
                ),
                "Sample Value": str(
                    self.raw_df[col]\
                        .dropna().iloc[0]
                ) if len(
                    self.raw_df[col].dropna()
                ) > 0 else "N/A"
            }
            summary.append(row)

        return pd.DataFrame(summary)

    def get_warnings(self):
        """Return load warnings"""
        return self.load_warnings

    def get_errors(self):
        """Return load errors"""
        return self.load_errors

    def is_loaded(self):
        """Check if data loaded"""
        return self.raw_df is not None


# ─────────────────────────────────────────
# SAMPLE DATASET LOADER
# For testing without uploading files
# ─────────────────────────────────────────

class SampleDataLoader:
    """
    Loads built-in sample datasets
    for testing and demonstration
    """

    @staticmethod
    def load_diabetes_sample():
        """
        Generate synthetic diabetes-like
        dataset for demonstration
        when no file is uploaded
        """
        np.random.seed(42)
        n = 200

        df = pd.DataFrame({
            "Pregnancies": np.random.randint(
                0, 17, n
            ),
            "Glucose": np.random.normal(
                120, 32, n
            ).clip(0, 200).astype(int),
            "BloodPressure": np.random.normal(
                69, 19, n
            ).clip(0, 122).astype(int),
            "SkinThickness": np.random.normal(
                20, 16, n
            ).clip(0, 99).astype(int),
            "Insulin": np.random.normal(
                79, 115, n
            ).clip(0, 846).astype(int),
            "BMI": np.random.normal(
                32, 7, n
            ).clip(0, 67).round(1),
            "DiabetesPedigreeFunction":
                np.random.exponential(
                    0.47, n
                ).clip(0.08, 2.42).round(3),
            "Age": np.random.randint(21, 81, n),
        })

        # Generate outcome based on
        # realistic risk factors
        risk_score = (
            (df["Glucose"] > 140).astype(int) +
            (df["BMI"] > 30).astype(int) +
            (df["Age"] > 45).astype(int)
        )
        df["Outcome"] = (
            risk_score >= 2
        ).astype(int)

        # Add some missing values
        # to make cleaning meaningful
        for col in [
            "Glucose", "BMI",
            "BloodPressure"
        ]:
            mask = np.random.random(n) < 0.05
            df.loc[mask, col] = 0

        return df

    @staticmethod
    def get_available_samples():
        """List available sample datasets"""
        return {
            "diabetes": {
                "name": "Diabetes Dataset",
                "description": (
                    "Patient health records "
                    "for diabetes prediction"
                ),
                "rows": 200,
                "columns": 9,
                "domain": "healthcare"
            }
        }

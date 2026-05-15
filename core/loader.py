# core/loader.py
# Handles dataset loading,
# validation, profiling,
# and sample dataset management

import pandas as pd
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

    # ─────────────────────────────────────
    # MAIN FILE LOADER
    # ─────────────────────────────────────

    def load(self, uploaded_file):

        self.load_errors = []
        self.load_warnings = []

        try:

            # Step 1 — Extract metadata
            self.file_info = \
                self._extract_file_info(
                    uploaded_file
                )

            # Step 2 — Read CSV
            df = self._read_csv(
                uploaded_file
            )

            if df is None:
                return (
                    None,
                    self.file_info,
                    self.load_errors
                )

            # Step 3 — Validate
            is_valid, error_msg = \
                validate_csv_file(df)

            if not is_valid:

                self.load_errors.append(
                    error_msg
                )

                return (
                    None,
                    self.file_info,
                    self.load_errors
                )

            # Step 4 — Build dataset info
            self.file_info.update(
                self._build_dataset_info(df)
            )

            # Step 5 — Store dataframe
            self.raw_df = df

            return (
                df,
                self.file_info,
                self.load_errors
            )

        except Exception as e:

            self.load_errors.append(
                f"Failed to load file: {str(e)}"
            )

            return (
                None,
                self.file_info,
                self.load_errors
            )

    # ─────────────────────────────────────
    # EXTRACT FILE INFO
    # ─────────────────────────────────────

    def _extract_file_info(self, file):

        return {

            "filename": file.name,

            "file_size":
                get_file_size(file),

            "file_hash":
                get_file_hash(file),

            "file_type":
                file.name.split(".")[-1].upper()
        }

    # ─────────────────────────────────────
    # READ CSV FILE
    # ─────────────────────────────────────

    def _read_csv(self, uploaded_file):

        encodings = [
            "utf-8",
            "latin-1",
            "iso-8859-1",
            "cp1252"
        ]

        for encoding in encodings:

            try:

                uploaded_file.seek(0)

                df = pd.read_csv(
                    uploaded_file,
                    encoding=encoding
                )

                if encoding != "utf-8":

                    self.load_warnings.append(
                        f"Loaded using "
                        f"{encoding} encoding"
                    )

                return df

            except UnicodeDecodeError:
                continue

            except pd.errors.EmptyDataError:

                self.load_errors.append(
                    "Uploaded file is empty"
                )

                return None

            except pd.errors.ParserError:

                try:

                    uploaded_file.seek(0)

                    df = pd.read_csv(
                        uploaded_file,
                        sep=";",
                        encoding=encoding
                    )

                    self.load_warnings.append(
                        "Semicolon separator detected"
                    )

                    return df

                except Exception:
                    continue

        self.load_errors.append(
            "Could not read CSV file"
        )

        return None

    # ─────────────────────────────────────
    # BUILD DATASET PROFILE
    # ─────────────────────────────────────

    def _build_dataset_info(self, df):

        domain, confidence = \
            detect_dataset_domain(df)

        numeric_cols = \
            get_numeric_columns(df)

        categorical_cols = \
            get_categorical_columns(df)

        binary_cols = \
            get_binary_columns(df)

        # Column type map
        column_types = {}

        for col in df.columns:

            column_types[col] = \
                detect_column_type(
                    df,
                    col
                )

        # Missing values
        total_cells = \
            df.shape[0] * df.shape[1]

        missing_count = \
            int(df.isna().sum().sum())

        missing_pct = round(
            (missing_count / total_cells) * 100,
            1
        )

        # Duplicate rows
        duplicate_count = \
            int(df.duplicated().sum())

        # Memory usage
        memory_usage = \
            df.memory_usage(
                deep=True
            ).sum() / 1024

        return {

            "rows":
                len(df),

            "columns":
                len(df.columns),

            "numeric_columns":
                numeric_cols,

            "categorical_columns":
                categorical_cols,

            "binary_columns":
                binary_cols,

            "column_types":
                column_types,

            "missing_count":
                missing_count,

            "missing_pct":
                missing_pct,

            "duplicate_count":
                duplicate_count,

            "domain":
                domain,

            "domain_confidence":
                confidence,

            "domain_icon":
                get_domain_icon(domain),

            "column_names":
                df.columns.tolist(),

            "memory_usage":
                f"{memory_usage:.1f} KB"
        }

    # ─────────────────────────────────────
    # SAMPLE DATA
    # ─────────────────────────────────────

    def get_sample(self, n=5):

        if self.raw_df is not None:
            return self.raw_df.head(n)

        return None

    # ─────────────────────────────────────
    # COLUMN SUMMARY
    # ─────────────────────────────────────

    def get_column_summary(self):

        if self.raw_df is None:
            return pd.DataFrame()

        summary = []

        for col in self.raw_df.columns:

            summary.append({

                "Column":
                    col,

                "Type":
                    detect_column_type(
                        self.raw_df,
                        col
                    ),

                "Missing":
                    int(
                        self.raw_df[col]
                        .isna()
                        .sum()
                    ),

                "Missing %":
                    round(
                        (
                            self.raw_df[col]
                            .isna()
                            .sum()
                            /
                            len(self.raw_df)
                        ) * 100,
                        1
                    ),

                "Unique Values":
                    int(
                        self.raw_df[col]
                        .nunique()
                    ),

                "Sample Value":
                    str(
                        self.raw_df[col]
                        .dropna()
                        .iloc[0]
                    )
                    if len(
                        self.raw_df[col]
                        .dropna()
                    ) > 0
                    else "N/A"
            })

        return pd.DataFrame(summary)

    # ─────────────────────────────────────
    # GETTERS
    # ─────────────────────────────────────

    def get_warnings(self):

        return self.load_warnings

    def get_errors(self):

        return self.load_errors

    def is_loaded(self):

        return self.raw_df is not None


# ─────────────────────────────────────────
# SAMPLE DATASET LOADER
# ─────────────────────────────────────────

class SampleDataLoader:
    """
    Loads built-in sample datasets
    from sample_data folder
    """

    DATASETS = {
        "diabetes": "sample_data/diabetes.csv",
        "heart": "sample_data/heart.csv",
        "hospital": "sample_data/hospital.csv"
    }

    @staticmethod
    def load_sample_dataset(name):

        name = name.lower()

        if name not in \
                SampleDataLoader.DATASETS:
            raise ValueError(
                f"Dataset '{name}' not found"
            )

        path = \
            SampleDataLoader.DATASETS[name]

        return pd.read_csv(path)

    @staticmethod
    def get_available_samples():

        return {
            "diabetes": {
                "name": "Diabetes Dataset",
                "domain": "healthcare"
            },
            "heart": {
                "name": "Heart Disease Dataset",
                "domain": "healthcare"
            },
            "hospital": {
                "name": "Hospital Dataset",
                "domain": "healthcare"
            }
        }

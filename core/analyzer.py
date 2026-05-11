import pandas as pd
import numpy as np

class DataAnalyzer:
    def __init__(self, df):
        self.df = df
        self.numeric_cols = \
            df.select_dtypes(
                include=["float64", "int64"]
            ).columns.tolist()
        self.categorical_cols = \
            df.select_dtypes(
                include=["object"]
            ).columns.tolist()

    def get_overview(self):
        """Complete dataset overview"""
        return {
            "total_rows": len(self.df),
            "total_columns": len(self.df.columns),
            "numeric_columns": len(
                self.numeric_cols
            ),
            "categorical_columns": len(
                self.categorical_cols
            ),
            "missing_values": int(
                self.df.isna().sum().sum()
            ),
            "duplicate_rows": int(
                self.df.duplicated().sum()
            ),
            "memory_usage": f"{self.df.memory_usage(deep=True).sum() / 1024:.1f} KB"
        }

    def get_statistics(self):
        """Statistics for numeric columns"""
        if not self.numeric_cols:
            return pd.DataFrame()
        return self.df[
            self.numeric_cols
        ].describe().round(2)

    def get_correlations(self):
        """Correlation matrix"""
        if len(self.numeric_cols) < 2:
            return pd.DataFrame()
        return self.df[
            self.numeric_cols
        ].corr().round(2)

    def get_column_info(self):
        """Detailed per-column info"""
        info = []
        for col in self.df.columns:
            col_data = {
                "column": col,
                "dtype": str(
                    self.df[col].dtype
                ),
                "missing": int(
                    self.df[col].isna().sum()
                ),
                "missing_pct": round(
                    self.df[col].isna().sum() /
                    len(self.df) * 100, 1
                ),
                "unique_values": int(
                    self.df[col].nunique()
                )
            }

            # Add numeric stats
            if self.df[col].dtype in [
                "float64", "int64"
            ]:
                col_data.update({
                    "mean": round(
                        float(
                            self.df[col].mean()
                        ), 2
                    ),
                    "median": round(
                        float(
                            self.df[col].median()
                        ), 2
                    ),
                    "std": round(
                        float(
                            self.df[col].std()
                        ), 2
                    ),
                    "min": round(
                        float(
                            self.df[col].min()
                        ), 2
                    ),
                    "max": round(
                        float(
                            self.df[col].max()
                        ), 2
                    )
                })
            info.append(col_data)

        return pd.DataFrame(info)

    def detect_target_column(self):
        """
        Auto detect likely target column
        for classification datasets
        """
        # Common target column names
        target_keywords = [
            "outcome", "target", "label",
            "class", "result", "diagnosis",
            "disease", "status"
        ]
        for col in self.df.columns:
            if any(
                keyword in col.lower()
                for keyword in target_keywords
            ):
                return col

        # Check for binary columns
        for col in self.numeric_cols:
            if self.df[col].nunique() == 2:
                vals = sorted(
                    self.df[col].unique()
                )
                if vals == [0, 1]:
                    return col
        return None

    def get_target_analysis(self, target_col):
        """Analyze target column distribution"""
        if target_col not in self.df.columns:
            return {}

        counts = self.df[
            target_col
        ].value_counts()

        return {
            "distribution": counts.to_dict(),
            "percentages": (
                counts / len(self.df) * 100
            ).round(1).to_dict(),
            "is_balanced": (
                counts.min() / counts.max() > 0.4
            )
        }

    def get_outliers(self):
        """Detect outliers using IQR method"""
        outlier_info = {}
        for col in self.numeric_cols:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR

            outliers = self.df[
                (self.df[col] < lower) |
                (self.df[col] > upper)
            ]

            if len(outliers) > 0:
                outlier_info[col] = {
                    "count": len(outliers),
                    "percentage": round(
                        len(outliers) /
                        len(self.df) * 100, 1
                    ),
                    "lower_bound": round(
                        lower, 2
                    ),
                    "upper_bound": round(
                        upper, 2
                    )
                }
        return outlier_info
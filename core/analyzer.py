# core/analyzer.py

import pandas as pd
import numpy as np


class DataAnalyzer:

    def __init__(self, df):

        self.df = df.copy()

        self.numeric_cols = (
            self.df.select_dtypes(
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

        self.categorical_cols = (
            self.df.select_dtypes(
                include=[
                    "object",
                    "category",
                    "bool"
                ]
            )
            .columns
            .tolist()
        )

    # ─────────────────────────────────────
    # DATASET OVERVIEW
    # ─────────────────────────────────────

    def get_overview(self):

        return {

            "total_rows":
                len(self.df),

            "total_columns":
                len(self.df.columns),

            "numeric_columns":
                len(self.numeric_cols),

            "categorical_columns":
                len(self.categorical_cols),

            "missing_values":
                int(
                    self.df
                    .isna()
                    .sum()
                    .sum()
                ),

            "duplicate_rows":
                int(
                    self.df
                    .duplicated()
                    .sum()
                ),

            "memory_usage":
                (
                    f"{self.df.memory_usage(deep=True).sum() / 1024:.1f} KB"
                )
        }

    # ─────────────────────────────────────
    # DESCRIPTIVE STATISTICS
    # ─────────────────────────────────────

    def get_statistics(self):

        if not self.numeric_cols:
            return pd.DataFrame()

        return (
            self.df[self.numeric_cols]
            .describe()
            .round(2)
        )

    # ─────────────────────────────────────
    # CORRELATION MATRIX
    # ─────────────────────────────────────

    def get_correlations(self):

        if len(self.numeric_cols) < 2:
            return pd.DataFrame()

        return (
            self.df[self.numeric_cols]
            .corr()
            .round(2)
        )

    # ─────────────────────────────────────
    # TOP CORRELATIONS
    # ─────────────────────────────────────

    def get_top_correlations(
        self,
        top_n=10
    ):

        corr = self.get_correlations()

        if corr.empty:
            return pd.DataFrame()

        correlations = []

        for i in range(len(corr.columns)):

            for j in range(
                i + 1,
                len(corr.columns)
            ):

                col1 = corr.columns[i]
                col2 = corr.columns[j]

                value = corr.iloc[i, j]

                correlations.append({

                    "column_1":
                        col1,

                    "column_2":
                        col2,

                    "correlation":
                        round(value, 2),

                    "abs_correlation":
                        abs(
                            round(value, 2)
                        )
                })

        corr_df = pd.DataFrame(correlations)

        return (
            corr_df
            .sort_values(
                by="abs_correlation",
                ascending=False
            )
            .head(top_n)
        )

    # ─────────────────────────────────────
    # COLUMN INFORMATION
    # ─────────────────────────────────────

    def get_column_info(self):

        info = []

        for col in self.df.columns:

            col_data = {

                "column":
                    col,

                "dtype":
                    str(
                        self.df[col].dtype
                    ),

                "missing":
                    int(
                        self.df[col]
                        .isna()
                        .sum()
                    ),

                "missing_pct":
                    round(
                        (
                            self.df[col]
                            .isna()
                            .sum()
                            / len(self.df)
                        ) * 100,
                        2
                    ),

                "unique_values":
                    int(
                        self.df[col]
                        .nunique()
                    )
            }

            if col in self.numeric_cols:

                col_data.update({

                    "mean":
                        round(
                            float(
                                self.df[col]
                                .mean()
                            ),
                            2
                        ),

                    "median":
                        round(
                            float(
                                self.df[col]
                                .median()
                            ),
                            2
                        ),

                    "std":
                        round(
                            float(
                                self.df[col]
                                .std()
                            ),
                            2
                        ),

                    "min":
                        round(
                            float(
                                self.df[col]
                                .min()
                            ),
                            2
                        ),

                    "max":
                        round(
                            float(
                                self.df[col]
                                .max()
                            ),
                            2
                        ),

                    "skewness":
                        round(
                            float(
                                self.df[col]
                                .skew()
                            ),
                            2
                        ),

                    "kurtosis":
                        round(
                            float(
                                self.df[col]
                                .kurtosis()
                            ),
                            2
                        )
                })

            info.append(col_data)

        return pd.DataFrame(info)

    # ─────────────────────────────────────
    # TARGET COLUMN DETECTION
    # ─────────────────────────────────────

    def detect_target_column(self):

        target_keywords = [

            "outcome",
            "target",
            "label",
            "class",
            "result",
            "diagnosis",
            "disease",
            "status"

        ]

        for col in self.df.columns:

            if any(
                keyword in col.lower()
                for keyword
                in target_keywords
            ):
                return col

        for col in self.numeric_cols:

            unique_vals = (
                self.df[col]
                .dropna()
                .unique()
            )

            if len(unique_vals) == 2:

                vals = sorted(unique_vals)

                if vals == [0, 1]:
                    return col

        return None

    # ─────────────────────────────────────
    # TARGET ANALYSIS
    # ─────────────────────────────────────

    def get_target_analysis(
        self,
        target_col
    ):

        if target_col \
                not in self.df.columns:
            return {}

        counts = (
            self.df[target_col]
            .value_counts()
        )

        return {

            "distribution":
                counts.to_dict(),

            "percentages":
                (
                    counts /
                    len(self.df) * 100
                )
                .round(1)
                .to_dict(),

            "is_balanced":
                (
                    counts.min()
                    / counts.max()
                ) > 0.4
        }

    # ─────────────────────────────────────
    # OUTLIER DETECTION
    # ─────────────────────────────────────

    def get_outliers(self):

        outlier_info = {}

        for col in self.numeric_cols:

            Q1 = (
                self.df[col]
                .quantile(0.25)
            )

            Q3 = (
                self.df[col]
                .quantile(0.75)
            )

            IQR = Q3 - Q1

            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR

            outliers = self.df[
                (
                    self.df[col] < lower
                ) |
                (
                    self.df[col] > upper
                )
            ]

            if len(outliers) > 0:

                outlier_info[col] = {

                    "count":
                        len(outliers),

                    "percentage":
                        round(
                            (
                                len(outliers)
                                / len(self.df)
                            ) * 100,
                            2
                        ),

                    "lower_bound":
                        round(
                            lower,
                            2
                        ),

                    "upper_bound":
                        round(
                            upper,
                            2
                        )
                }

        return outlier_info

    # ─────────────────────────────────────
    # QUALITY SCORE
    # ─────────────────────────────────────

    def calculate_quality_score(self):

        score = 100

        missing_pct = (
            self.df
            .isna()
            .sum()
            .sum()
            /
            (
                len(self.df)
                * len(self.df.columns)
            )
        ) * 100

        duplicate_pct = (
            self.df
            .duplicated()
            .sum()
            / len(self.df)
        ) * 100

        outlier_penalty = 0

        outliers = self.get_outliers()

        for _, details \
                in outliers.items():

            outlier_penalty += (
                details["percentage"] * 0.2
            )

        score -= missing_pct * 0.5
        score -= duplicate_pct * 0.3
        score -= outlier_penalty

        score = max(
            0,
            min(100, score)
        )

        return {

            "overall_score":
                round(score, 1),

            "missing_penalty":
                round(
                    missing_pct,
                    2
                ),

            "duplicate_penalty":
                round(
                    duplicate_pct,
                    2
                ),

            "outlier_penalty":
                round(
                    outlier_penalty,
                    2
                )
        }

    # ─────────────────────────────────────
    # DISTRIBUTION ANALYSIS
    # ─────────────────────────────────────

    def get_distribution_analysis(self):

        results = []

        for col in self.numeric_cols:

            skewness = (
                self.df[col]
                .skew()
            )

            kurtosis = (
                self.df[col]
                .kurtosis()
            )

            distribution = "normal"

            if abs(skewness) > 1:

                distribution = \
                    "highly_skewed"

            elif abs(skewness) > 0.5:

                distribution = \
                    "moderately_skewed"

            results.append({

                "column":
                    col,

                "skewness":
                    round(
                        skewness,
                        2
                    ),

                "kurtosis":
                    round(
                        kurtosis,
                        2
                    ),

                "distribution":
                    distribution
            })

        return pd.DataFrame(results)

    # ─────────────────────────────────────
    # DATASET HEALTH REPORT
    # ─────────────────────────────────────

    def generate_health_report(self):

        quality = \
            self.calculate_quality_score()

        outliers = \
            self.get_outliers()

        issues = []

        if quality[
            "missing_penalty"
        ] > 10:

            issues.append(
                "High missing values detected"
            )

        if quality[
            "duplicate_penalty"
        ] > 5:

            issues.append(
                "High duplicate rows detected"
            )

        if len(outliers) > 0:

            issues.append(
                "Outliers detected in numeric columns"
            )

        if len(issues) == 0:

            issues.append(
                "Dataset health looks good"
            )

        return {

            "quality_score":
                quality[
                    "overall_score"
                ],

            "issues":
                issues,

            "total_outlier_columns":
                len(outliers),

            "recommended_action":
                (
                    "Dataset ready for analysis"
                    if quality[
                        "overall_score"
                    ] >= 80
                    else
                    "Cleaning recommended before analysis"
                )
        }

    # ─────────────────────────────────────
    # DATASET SUMMARY
    # ─────────────────────────────────────

    def get_dataset_summary(self):

        overview = \
            self.get_overview()

        quality = \
            self.calculate_quality_score()

        target = \
            self.detect_target_column()

        return {

            "rows":
                overview["total_rows"],

            "columns":
                overview["total_columns"],

            "missing_values":
                overview["missing_values"],

            "duplicates":
                overview["duplicate_rows"],

            "quality_score":
                quality["overall_score"],

            "target_column":
                target,

            "numeric_columns":
                self.numeric_cols,

            "categorical_columns":
                self.categorical_cols
        }

    # ─────────────────────────────────────
    # ANALYTICS RECOMMENDATIONS
    # ─────────────────────────────────────

    def get_recommendations(self):

        recommendations = []

        quality = \
            self.calculate_quality_score()

        if quality[
            "overall_score"
        ] < 70:

            recommendations.append(
                "Dataset cleaning recommended"
            )

        if len(
            self.get_outliers()
        ) > 0:

            recommendations.append(
                "Review outliers before modeling"
            )

        if len(self.numeric_cols) >= 2:

            recommendations.append(
                "Correlation analysis available"
            )

        target = \
            self.detect_target_column()

        if target:

            recommendations.append(
                f"Target column detected: {target}"
            )

        if len(recommendations) == 0:

            recommendations.append(
                "Dataset looks healthy for analysis"
            )

        return recommendations

    # ─────────────────────────────────────
    # DASHBOARD METRICS
    # ─────────────────────────────────────

    def get_dashboard_metrics(self):

        quality = \
            self.calculate_quality_score()

        return {

            "rows":
                len(self.df),

            "columns":
                len(self.df.columns),

            "quality_score":
                quality["overall_score"],

            "missing_values":
                int(
                    self.df
                    .isna()
                    .sum()
                    .sum()
                ),

            "duplicates":
                int(
                    self.df
                    .duplicated()
                    .sum()
                ),

            "outlier_columns":
                len(
                    self.get_outliers()
                )
        }

    # ─────────────────────────────────────
    # EXPORT SUMMARY
    # ─────────────────────────────────────

    def export_summary(self):

        return {

            "overview":
                self.get_overview(),

            "quality":
                self.calculate_quality_score(),

            "health":
                self.generate_health_report(),

            "recommendations":
                self.get_recommendations()
        }

    # ─────────────────────────────────────
    # DATA SAMPLE
    # ─────────────────────────────────────

    def get_sample(
        self,
        rows=5
    ):

        return self.df.head(rows)
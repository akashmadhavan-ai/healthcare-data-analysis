# core/insights.py

import pandas as pd
import numpy as np


class InsightGenerator:

    def __init__(
        self,
        df,
        analyzer
    ):

        self.df = df

        self.analyzer = analyzer

        self.insights = []

    # ─────────────────────────────────────
    # GENERATE ALL INSIGHTS
    # ─────────────────────────────────────

    def generate_all(
        self,
        target_col=None
    ):

        self.insights = []

        self._dataset_insights()

        self._quality_insights()

        self._distribution_insights()

        self._correlation_insights(
            target_col
        )

        self._outlier_insights()

        self._recommendation_insights()

        if target_col:

            self._target_insights(
                target_col
            )

        return self.insights

    # ─────────────────────────────────────
    # DATASET INSIGHTS
    # ─────────────────────────────────────

    def _dataset_insights(self):

        overview = \
            self.analyzer.get_overview()

        self.insights.append({

            "type":
                "info",

            "title":
                "Dataset Overview",

            "message":
                (
                    f"Dataset contains "
                    f"{overview['total_rows']:,} "
                    f"records and "
                    f"{overview['total_columns']} "
                    f"features "
                    f"({overview['numeric_columns']} "
                    f"numeric, "
                    f"{overview['categorical_columns']} "
                    f"categorical)."
                )
        })

        if overview[
            "missing_values"
        ] > 0:

            self.insights.append({

                "type":
                    "warning",

                "title":
                    "Missing Data Detected",

                "message":
                    (
                        f"{overview['missing_values']} "
                        f"missing values found. "
                        f"Dataset cleaning is "
                        f"recommended before "
                        f"advanced analysis."
                    )
            })

        else:

            self.insights.append({

                "type":
                    "success",

                "title":
                    "No Missing Data",

                "message":
                    (
                        "Dataset contains "
                        "no missing values."
                    )
            })

    # ─────────────────────────────────────
    # QUALITY INSIGHTS
    # ─────────────────────────────────────

    def _quality_insights(self):

        quality = \
            self.analyzer.calculate_quality_score()

        score = \
            quality[
                "overall_score"
            ]

        if score >= 90:

            insight_type = "success"

            status = \
                "excellent"

        elif score >= 80:

            insight_type = "info"

            status = "good"

        elif score >= 70:

            insight_type = "warning"

            status = "moderate"

        else:

            insight_type = "danger"

            status = "poor"

        self.insights.append({

            "type":
                insight_type,

            "title":
                "Dataset Quality Score",

            "message":
                (
                    f"Dataset quality score is "
                    f"{score}/100 "
                    f"({status} quality)."
                )
        })

    # ─────────────────────────────────────
    # DISTRIBUTION INSIGHTS
    # ─────────────────────────────────────

    def _distribution_insights(self):

        stats = \
            self.analyzer.get_statistics()

        if stats.empty:
            return

        for col in stats.columns:

            mean = stats[col]["mean"]

            std = stats[col]["std"]

            cv = (
                (
                    std / mean
                ) * 100
                if mean != 0
                else 0
            )

            # High variation

            if cv > 50:

                self.insights.append({

                    "type":
                        "warning",

                    "title":
                        f"High Variation in {col}",

                    "message":
                        (
                            f"'{col}' shows "
                            f"high variability "
                            f"(CV={cv:.1f}%). "
                            f"Consider reviewing "
                            f"potential outliers."
                        )
                })

            # Skewness detection

            skewness = float(
                self.df[col]
                .dropna()
                .skew()
            )

            if abs(skewness) > 1:

                direction = (
                    "right-skewed"
                    if skewness > 0
                    else "left-skewed"
                )

                self.insights.append({

                    "type":
                        "info",

                    "title":
                        f"Skewed Distribution: {col}",

                    "message":
                        (
                            f"'{col}' is "
                            f"{direction} "
                            f"(skewness="
                            f"{skewness:.2f})."
                        )
                })

    # ─────────────────────────────────────
    # CORRELATION INSIGHTS
    # ─────────────────────────────────────

    def _correlation_insights(
        self,
        target_col=None
    ):

        corr = \
            self.analyzer.get_correlations()

        if corr.empty:
            return

        # Target correlations

        if target_col and \
                target_col in corr.columns:

            target_corr = (
                corr[target_col]
                .drop(target_col)
                .abs()
            )

            if not target_corr.empty:

                top_predictor = \
                    target_corr.idxmax()

                top_value = \
                    target_corr.max()

                if top_value > 0.3:

                    self.insights.append({

                        "type":
                            "success",

                        "title":
                            "Strong Predictor Found",

                        "message":
                            (
                                f"'{top_predictor}' "
                                f"is strongly related "
                                f"to '{target_col}' "
                                f"(r={top_value:.2f})."
                            )
                    })

        # Strong correlations

        for i in range(
            len(corr.columns)
        ):

            for j in range(
                i + 1,
                len(corr.columns)
            ):

                col1 = corr.columns[i]
                col2 = corr.columns[j]

                value = abs(
                    corr.iloc[i, j]
                )

                if value > 0.7:

                    self.insights.append({

                        "type":
                            "warning",

                        "title":
                            "Strong Correlation",

                        "message":
                            (
                                f"'{col1}' and "
                                f"'{col2}' are "
                                f"strongly correlated "
                                f"(r={value:.2f})."
                            )
                    })

    # ─────────────────────────────────────
    # OUTLIER INSIGHTS
    # ─────────────────────────────────────

    def _outlier_insights(self):

        outliers = \
            self.analyzer.get_outliers()

        if not outliers:

            self.insights.append({

                "type":
                    "success",

                "title":
                    "No Significant Outliers",

                "message":
                    (
                        "No major outliers "
                        "detected in numeric columns."
                    )
            })

            return

        for col, info in \
                outliers.items():

            if info[
                "percentage"
            ] > 5:

                self.insights.append({

                    "type":
                        "warning",

                    "title":
                        f"Outliers Detected in {col}",

                    "message":
                        (
                            f"{info['count']} "
                            f"outliers found "
                            f"({info['percentage']}%)."
                        )
                })

    # ─────────────────────────────────────
    # TARGET INSIGHTS
    # ─────────────────────────────────────

    def _target_insights(
        self,
        target_col
    ):

        target_analysis = \
            self.analyzer.get_target_analysis(
                target_col
            )

        if not target_analysis:
            return

        dist = \
            target_analysis[
                "distribution"
            ]

        percentages = \
            target_analysis[
                "percentages"
            ]

        summary = " | ".join([

            (
                f"Class {k}: "
                f"{v} "
                f"({percentages.get(k, 0):.1f}%)"
            )

            for k, v
            in dist.items()
        ])

        self.insights.append({

            "type":
                "info",

            "title":
                "Target Distribution",

            "message":
                (
                    f"'{target_col}' "
                    f"distribution: "
                    f"{summary}"
                )
        })

        if not target_analysis[
            "is_balanced"
        ]:

            self.insights.append({

                "type":
                    "warning",

                "title":
                    "Class Imbalance Detected",

                "message":
                    (
                        f"'{target_col}' "
                        f"is imbalanced. "
                        f"This may affect "
                        f"predictive modeling."
                    )
            })

    # ─────────────────────────────────────
    # RECOMMENDATION INSIGHTS
    # ─────────────────────────────────────

    def _recommendation_insights(self):

        recommendations = \
            self.analyzer.get_recommendations()

        for recommendation \
                in recommendations:

            self.insights.append({

                "type":
                    "recommendation",

                "title":
                    "Recommendation",

                "message":
                    recommendation
            })

    # ─────────────────────────────────────
    # INSIGHT SUMMARY
    # ─────────────────────────────────────

    def get_summary(self):

        return {

            "total_insights":
                len(self.insights),

            "info":
                len([
                    i for i
                    in self.insights
                    if i["type"] == "info"
                ]),

            "success":
                len([
                    i for i
                    in self.insights
                    if i["type"] == "success"
                ]),

            "warning":
                len([
                    i for i
                    in self.insights
                    if i["type"] == "warning"
                ]),

            "recommendations":
                len([
                    i for i
                    in self.insights
                    if i["type"] ==
                    "recommendation"
                ])
        }

    # ─────────────────────────────────────
    # GET INSIGHTS BY TYPE
    # ─────────────────────────────────────

    def get_by_type(
        self,
        insight_type
    ):

        return [

            insight
            for insight
            in self.insights

            if insight["type"]
            == insight_type
        ]

    # ─────────────────────────────────────
    # EXPORT INSIGHTS
    # ─────────────────────────────────────

    def export_insights(self):

        return {

            "summary":
                self.get_summary(),

            "insights":
                self.insights
        }
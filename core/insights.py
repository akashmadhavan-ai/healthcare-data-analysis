import pandas as pd
import numpy as np

class InsightGenerator:
    def __init__(self, df, analyzer):
        self.df = df
        self.analyzer = analyzer
        self.insights = []

    def generate_all(self, target_col=None):
        """Generate all insights automatically"""
        self.insights = []

        self._dataset_insights()
        self._distribution_insights()
        self._correlation_insights(target_col)
        self._outlier_insights()

        if target_col:
            self._target_insights(target_col)

        return self.insights

    def _dataset_insights(self):
        """Basic dataset level insights"""
        overview = self.analyzer.get_overview()

        self.insights.append({
            "type": "info",
            "title": "Dataset Overview",
            "message": (
                f"Dataset contains "
                f"{overview['total_rows']:,} records "
                f"and {overview['total_columns']} features "
                f"({overview['numeric_columns']} numeric, "
                f"{overview['categorical_columns']} categorical)."
            )
        })

        if overview["missing_values"] > 0:
            self.insights.append({
                "type": "warning",
                "title": "Missing Data Detected",
                "message": (
                    f"{overview['missing_values']} missing "
                    f"values found and automatically "
                    f"handled using median/mode imputation."
                )
            })
        else:
            self.insights.append({
                "type": "success",
                "title": "No Missing Data",
                "message": (
                    "Dataset is complete with "
                    "no missing values."
                )
            })

    def _distribution_insights(self):
        """Insights from distributions"""
        stats = self.analyzer.get_statistics()
        if stats.empty:
            return

        for col in stats.columns:
            mean = stats[col]["mean"]
            std = stats[col]["std"]
            cv = (std / mean * 100
                  if mean != 0 else 0)

            # High variation
            if cv > 50:
                self.insights.append({
                    "type": "warning",
                    "title": f"High Variation in {col}",
                    "message": (
                        f"'{col}' shows high variability "
                        f"(CV={cv:.1f}%). "
                        f"Values range from "
                        f"{stats[col]['min']:.1f} to "
                        f"{stats[col]['max']:.1f}. "
                        f"Consider investigating outliers."
                    )
                })

            # Skewed distribution check
            col_data = self.df[col].dropna()
            skewness = float(col_data.skew())
            if abs(skewness) > 1:
                direction = (
                    "right (positive)"
                    if skewness > 0
                    else "left (negative)"
                )
                self.insights.append({
                    "type": "info",
                    "title": f"{col} is Skewed",
                    "message": (
                        f"'{col}' is skewed {direction} "
                        f"(skewness={skewness:.2f}). "
                        f"Median ({stats[col]['50%']:.2f}) "
                        f"is a better central measure "
                        f"than mean ({mean:.2f})."
                    )
                })

    def _correlation_insights(
        self, target_col=None
    ):
        """Insights from correlations"""
        corr = self.analyzer.get_correlations()
        if corr.empty:
            return

        if target_col and \
           target_col in corr.columns:
            # Find strongest predictors
            target_corr = corr[
                target_col
            ].drop(target_col).abs()
            top_predictor = target_corr.idxmax()
            top_value = target_corr.max()

            if top_value > 0.3:
                self.insights.append({
                    "type": "success",
                    "title": "Strongest Predictor Found",
                    "message": (
                        f"'{top_predictor}' is the "
                        f"strongest predictor of "
                        f"'{target_col}' "
                        f"(correlation={top_value:.2f}). "
                        f"This feature should be "
                        f"prioritized in analysis."
                    )
                })

        # Find any strong correlations
        for i in range(len(corr.columns)):
            for j in range(i + 1, len(
                corr.columns
            )):
                col1 = corr.columns[i]
                col2 = corr.columns[j]
                val = abs(corr.iloc[i, j])

                if val > 0.7:
                    self.insights.append({
                        "type": "warning",
                        "title": "Strong Correlation",
                        "message": (
                            f"'{col1}' and '{col2}' "
                            f"are strongly correlated "
                            f"(r={val:.2f}). "
                            f"These features may "
                            f"carry similar information."
                        )
                    })

    def _outlier_insights(self):
        """Insights from outliers"""
        outliers = self.analyzer.get_outliers()
        if not outliers:
            self.insights.append({
                "type": "success",
                "title": "No Significant Outliers",
                "message": (
                    "All numeric columns are "
                    "within expected ranges."
                )
            })
            return

        for col, info in outliers.items():
            if info["percentage"] > 5:
                self.insights.append({
                    "type": "warning",
                    "title": f"Outliers in {col}",
                    "message": (
                        f"'{col}' has "
                        f"{info['count']} outliers "
                        f"({info['percentage']}% of data). "
                        f"Expected range: "
                        f"{info['lower_bound']} to "
                        f"{info['upper_bound']}."
                    )
                })

    def _target_insights(self, target_col):
        """Insights about the target column"""
        target_analysis = \
            self.analyzer.get_target_analysis(
                target_col
            )

        if not target_analysis:
            return

        dist = target_analysis["distribution"]
        pcts = target_analysis["percentages"]

        # Class distribution
        summary = " | ".join([
            f"Class {k}: {v} "
            f"({pcts.get(k, 0):.1f}%)"
            for k, v in dist.items()
        ])

        self.insights.append({
            "type": "info",
            "title": f"Target Distribution",
            "message": (
                f"'{target_col}' distribution: "
                f"{summary}"
            )
        })

        # Class imbalance check
        if not target_analysis["is_balanced"]:
            self.insights.append({
                "type": "warning",
                "title": "Class Imbalance Detected",
                "message": (
                    f"'{target_col}' is imbalanced. "
                    f"This may affect model performance "
                    f"if used for machine learning."
                )
            })

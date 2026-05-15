# core/visualizer.py

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from plotly.subplots import (
    make_subplots
)


class DataVisualizer:

    def __init__(self, df):

        if df.empty:

            raise ValueError(
                "Input dataset is empty"
            )

        self.df = df.copy()

        self.numeric_cols = (
            self.df.select_dtypes(
                include=[
                    "float64",
                    "int64",
                    "float32",
                    "int32"
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

        # ─────────────────────────────
        # COLOR PALETTE
        # ─────────────────────────────

        self.colors = [

            "#2563EB",
            "#16A34A",
            "#DC2626",
            "#D97706",
            "#7C3AED",
            "#0891B2",
            "#DB2777",
            "#4B5563"

        ]

        self.template = "plotly_white"

    # ─────────────────────────────────────
    # HISTOGRAM
    # ─────────────────────────────────────

    def histogram(
        self,
        col,
        target=None
    ):

        if col not in self.df.columns:

            raise ValueError(
                f"Column '{col}' not found"
            )

        fig = px.histogram(

            self.df,

            x=col,

            color=target,

            title=f"Distribution of {col}",

            marginal="box",

            color_discrete_sequence=
            self.colors,

            template=self.template
        )

        fig.update_layout(

            showlegend=True,

            height=450
        )

        return fig

    # ─────────────────────────────────────
    # BOXPLOT
    # ─────────────────────────────────────

    def boxplot(
        self,
        col,
        target=None
    ):

        if col not in self.df.columns:

            raise ValueError(
                f"Column '{col}' not found"
            )

        fig = px.box(

            self.df,

            y=col,

            x=target,

            color=target,

            title=(
                f"{col} Distribution "
                f"by {target or 'Overall'}"
            ),

            color_discrete_sequence=
            self.colors,

            template=self.template
        )

        fig.update_layout(
            height=450
        )

        return fig

    # ─────────────────────────────────────
    # SCATTER PLOT
    # ─────────────────────────────────────

    def scatter(
        self,
        x_col,
        y_col,
        target=None
    ):

        if x_col \
                not in self.df.columns:

            raise ValueError(
                f"Column '{x_col}' not found"
            )

        if y_col \
                not in self.df.columns:

            raise ValueError(
                f"Column '{y_col}' not found"
            )

        fig = px.scatter(

            self.df,

            x=x_col,

            y=y_col,

            color=target,

            title=(
                f"{x_col} vs {y_col}"
            ),

            trendline="ols",

            color_discrete_sequence=
            self.colors,

            template=self.template
        )

        fig.update_layout(
            height=500
        )

        return fig

    # ─────────────────────────────────────
    # LINE CHART
    # ─────────────────────────────────────

    def line_chart(
        self,
        x_col,
        y_col,
        color=None
    ):

        fig = px.line(

            self.df,

            x=x_col,

            y=y_col,

            color=color,

            title=(
                f"{y_col} over {x_col}"
            ),

            color_discrete_sequence=
            self.colors,

            template=self.template
        )

        fig.update_layout(
            height=450
        )

        return fig

    # ─────────────────────────────────────
    # BAR CHART
    # ─────────────────────────────────────

    def bar_chart(
        self,
        x_col,
        y_col,
        color=None
    ):

        fig = px.bar(

            self.df,

            x=x_col,

            y=y_col,

            color=color,

            title=(
                f"{y_col} by {x_col}"
            ),

            color_discrete_sequence=
            self.colors,

            template=self.template
        )

        fig.update_layout(
            height=450
        )

        return fig

    # ─────────────────────────────────────
    # PIE CHART
    # ─────────────────────────────────────

    def pie_chart(
        self,
        column
    ):

        counts = (
            self.df[column]
            .value_counts()
        )

        fig = px.pie(

            values=counts.values,

            names=[
                str(v)
                for v in counts.index
            ],

            title=(
                f"{column} Distribution"
            ),

            color_discrete_sequence=
            self.colors,

            template=self.template
        )

        fig.update_layout(
            height=450
        )

        return fig

    # ─────────────────────────────────────
    # TARGET DISTRIBUTION
    # ─────────────────────────────────────

    def target_distribution(
        self,
        target_col
    ):

        return self.pie_chart(
            target_col
        )

    # ─────────────────────────────────────
    # CORRELATION HEATMAP
    # ─────────────────────────────────────

    def correlation_heatmap(self):

        if len(self.numeric_cols) < 2:

            return None

        corr = (
            self.df[
                self.numeric_cols
            ]
            .corr()
            .fillna(0)
        )

        fig = px.imshow(

            corr,

            title=(
                "Feature Correlation Matrix"
            ),

            color_continuous_scale=
            "RdBu_r",

            aspect="auto",

            template=self.template,

            text_auto=True
        )

        fig.update_layout(
            height=600
        )

        return fig

    # ─────────────────────────────────────
    # PAIRWISE SCATTER MATRIX
    # ─────────────────────────────────────

    def pairwise_scatter(
        self,
        target=None
    ):

        if len(self.numeric_cols) < 2:

            return None

        cols = [

            c for c
            in self.numeric_cols

            if c != target

        ][:5]

        fig = px.scatter_matrix(

            self.df,

            dimensions=cols,

            color=target,

            title=(
                "Pairwise Feature Analysis"
            ),

            color_discrete_sequence=
            self.colors,

            template=self.template
        )

        fig.update_layout(
            height=700
        )

        return fig

    # ─────────────────────────────────────
    # OUTLIER CHART
    # ─────────────────────────────────────

    def outlier_chart(
        self,
        outlier_info
    ):

        if not outlier_info:

            return None

        cols = list(
            outlier_info.keys()
        )

        counts = [

            outlier_info[c][
                "percentage"
            ]

            for c in cols
        ]

        fig = px.bar(

            x=cols,

            y=counts,

            title=(
                "Outlier Percentage "
                "by Column"
            ),

            labels={

                "x":
                    "Column",

                "y":
                    "Outlier %"
            },

            color=counts,

            color_continuous_scale=
            "Reds",

            template=self.template
        )

        fig.update_layout(
            height=450
        )

        return fig

    # ─────────────────────────────────────
    # MISSING VALUE CHART
    # ─────────────────────────────────────

    def missing_values_chart(self):

        missing = (
            self.df
            .isna()
            .sum()
        )

        missing = (
            missing[
                missing > 0
            ]
            .sort_values(
                ascending=False
            )
        )

        if missing.empty:

            return None

        fig = px.bar(

            x=missing.index,

            y=missing.values,

            title=(
                "Missing Values "
                "by Column"
            ),

            labels={

                "x":
                    "Column",

                "y":
                    "Missing Count"
            },

            color=missing.values,

            color_continuous_scale=
            "Oranges",

            template=self.template
        )

        fig.update_layout(
            height=450
        )

        return fig

    # ─────────────────────────────────────
    # ALL HISTOGRAMS
    # ─────────────────────────────────────

    def all_histograms(
        self,
        target=None
    ):

        charts = {}

        for col in self.numeric_cols:

            if col != target:

                charts[col] = (
                    self.histogram(
                        col,
                        target
                    )
                )

        return charts

    # ─────────────────────────────────────
    # ALL BOXPLOTS
    # ─────────────────────────────────────

    def all_boxplots(
        self,
        target=None
    ):

        charts = {}

        for col in self.numeric_cols:

            if col != target:

                charts[col] = (
                    self.boxplot(
                        col,
                        target
                    )
                )

        return charts

    # ─────────────────────────────────────
    # DASHBOARD SUMMARY FIGURE
    # ─────────────────────────────────────

    def dashboard_summary(
        self
    ):

        fig = make_subplots(

            rows=2,

            cols=2,

            subplot_titles=(

                "Missing Values",

                "Data Types",

                "Numeric Columns",

                "Categorical Columns"
            )
        )

        # Missing values

        missing = (
            self.df
            .isna()
            .sum()
            .sum()
        )

        fig.add_trace(

            go.Indicator(

                mode="number",

                value=missing,

                title={
                    "text":
                        "Missing Values"
                }

            ),

            row=1,
            col=1
        )

        # Data types

        fig.add_trace(

            go.Pie(

                labels=[
                    "Numeric",
                    "Categorical"
                ],

                values=[

                    len(
                        self.numeric_cols
                    ),

                    len(
                        self.categorical_cols
                    )
                ]
            ),

            row=1,
            col=2
        )

        # Numeric columns

        fig.add_trace(

            go.Bar(

                x=self.numeric_cols,

                y=[1] *
                len(self.numeric_cols),

                name="Numeric"
            ),

            row=2,
            col=1
        )

        # Categorical columns

        fig.add_trace(

            go.Bar(

                x=self.categorical_cols,

                y=[1] *
                len(
                    self.categorical_cols
                ),

                name="Categorical"
            ),

            row=2,
            col=2
        )

        fig.update_layout(

            height=700,

            title=(
                "Dataset Dashboard Summary"
            ),

            template=self.template
        )

        return fig

    # ─────────────────────────────────────
    # EXPORT CHART CONFIG
    # ─────────────────────────────────────

    def get_export_config(self):

        return {

            "displaylogo":
                False,

            "toImageButtonOptions": {

                "format":
                    "png",

                "filename":
                    "healthcare_chart",

                "height":
                    700,

                "width":
                    1200,

                "scale":
                    2
            }
        }
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

class DataVisualizer:
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

        # Color scheme
        self.colors = [
            "#2ecc71", "#e74c3c",
            "#3498db", "#f39c12",
            "#9b59b6", "#1abc9c"
        ]

    def histogram(self, col, target=None):
        """Dynamic histogram for any column"""
        fig = px.histogram(
            self.df,
            x=col,
            color=target,
            title=f"Distribution of {col}",
            marginal="box",
            color_discrete_sequence=self.colors,
            template="plotly_dark"
        )
        fig.update_layout(
            showlegend=True,
            height=400
        )
        return fig

    def boxplot(self, col, target=None):
        """Dynamic boxplot for any column"""
        fig = px.box(
            self.df,
            y=col,
            x=target,
            color=target,
            title=f"{col} Distribution "
                  f"by {target or 'Overall'}",
            color_discrete_sequence=self.colors,
            template="plotly_dark"
        )
        fig.update_layout(height=400)
        return fig

    def scatter(self, x_col, y_col,
                target=None):
        """Dynamic scatter for any two columns"""
        fig = px.scatter(
            self.df,
            x=x_col,
            y=y_col,
            color=target,
            title=f"{x_col} vs {y_col}",
            trendline="ols",
            color_discrete_sequence=self.colors,
            template="plotly_dark"
        )
        fig.update_layout(height=400)
        return fig

    def correlation_heatmap(self):
        """Correlation heatmap"""
        if len(self.numeric_cols) < 2:
            return None

        corr = self.df[
            self.numeric_cols
        ].corr()

        fig = px.imshow(
            corr,
            title="Feature Correlation Matrix",
            color_continuous_scale="RdBu_r",
            aspect="auto",
            template="plotly_dark",
            text_auto=True
        )
        fig.update_layout(height=500)
        return fig

    def target_distribution(self, target_col):
        """Pie chart for target column"""
        counts = self.df[
            target_col
        ].value_counts()

        fig = px.pie(
            values=counts.values,
            names=[str(n) for n in counts.index],
            title=f"{target_col} Distribution",
            color_discrete_sequence=self.colors,
            template="plotly_dark"
        )
        fig.update_layout(height=400)
        return fig

    def all_histograms(self, target=None):
        """
        AUTO-GENERATE histograms
        for ALL numeric columns
        This is the dynamic part
        """
        charts = {}
        for col in self.numeric_cols:
            if col != target:
                charts[col] = self.histogram(
                    col, target
                )
        return charts

    def all_boxplots(self, target=None):
        """
        AUTO-GENERATE boxplots
        for ALL numeric columns
        """
        charts = {}
        for col in self.numeric_cols:
            if col != target:
                charts[col] = self.boxplot(
                    col, target
                )
        return charts

    def pairwise_scatter(self, target=None):
        """Scatter matrix for all numeric"""
        if len(self.numeric_cols) < 2:
            return None

        cols = [
            c for c in self.numeric_cols
            if c != target
        ][:5]  # limit to 5 columns

        fig = px.scatter_matrix(
            self.df,
            dimensions=cols,
            color=target,
            title="Pairwise Feature Analysis",
            color_discrete_sequence=self.colors,
            template="plotly_dark"
        )
        fig.update_layout(height=600)
        return fig

    def outlier_chart(self, outlier_info):
        """Bar chart showing outlier counts"""
        if not outlier_info:
            return None

        cols = list(outlier_info.keys())
        counts = [
            outlier_info[c]["percentage"]
            for c in cols
        ]

        fig = px.bar(
            x=cols,
            y=counts,
            title="Outlier Percentage by Column",
            labels={
                "x": "Column",
                "y": "Outlier %"
            },
            color=counts,
            color_continuous_scale="Reds",
            template="plotly_dark"
        )
        fig.update_layout(height=400)
        return fig

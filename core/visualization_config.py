# core/visualization_config.py

import plotly.express as px
import plotly.graph_objects as go


class VisualizationConfig:

    def __init__(self):

        # ─────────────────────────────────
        # DEFAULT THEME
        # ─────────────────────────────────

        self.theme = "plotly_white"

        # ─────────────────────────────────
        # DEFAULT COLORS
        # ─────────────────────────────────

        self.color_palette = [

            "#2563EB",
            "#16A34A",
            "#DC2626",
            "#D97706",
            "#7C3AED",
            "#0891B2",
            "#DB2777",
            "#4B5563"

        ]

        # ─────────────────────────────────
        # DEFAULT CHART CONFIG
        # ─────────────────────────────────

        self.default_chart_config = {

            "template":
                self.theme,

            "height":
                500,

            "width":
                None,

            "showlegend":
                True,

            "margin":
                dict(
                    l=40,
                    r=40,
                    t=60,
                    b=40
                ),

            "font":
                dict(
                    family="Arial",
                    size=12
                )
        }

        # ─────────────────────────────────
        # DEFAULT EXPORT CONFIG
        # ─────────────────────────────────

        self.export_config = {

            "toImageButtonOptions": {

                "format":
                    "png",

                "filename":
                    "healthcare_visualization",

                "height":
                    800,

                "width":
                    1200,

                "scale":
                    2
            },

            "displaylogo":
                False
        }

    # ─────────────────────────────────────
    # APPLY STANDARD LAYOUT
    # ─────────────────────────────────────

    def apply_layout(

        self,

        fig,

        title="Chart",

        xaxis_title="",

        yaxis_title=""

    ):

        fig.update_layout(

            title=title,

            xaxis_title=xaxis_title,

            yaxis_title=yaxis_title,

            template=self.theme,

            height=self.default_chart_config[
                "height"
            ],

            showlegend=self.default_chart_config[
                "showlegend"
            ],

            margin=self.default_chart_config[
                "margin"
            ],

            font=self.default_chart_config[
                "font"
            ]
        )

        return fig

    # ─────────────────────────────────────
    # BAR CHART CONFIG
    # ─────────────────────────────────────

    def create_bar_chart(

        self,

        df,

        x,

        y,

        color=None,

        title="Bar Chart"

    ):

        fig = px.bar(

            df,

            x=x,

            y=y,

            color=color,

            color_discrete_sequence=
            self.color_palette

        )

        return self.apply_layout(

            fig,

            title=title,

            xaxis_title=x,

            yaxis_title=y
        )

    # ─────────────────────────────────────
    # LINE CHART CONFIG
    # ─────────────────────────────────────

    def create_line_chart(

        self,

        df,

        x,

        y,

        color=None,

        title="Line Chart"

    ):

        fig = px.line(

            df,

            x=x,

            y=y,

            color=color,

            color_discrete_sequence=
            self.color_palette

        )

        return self.apply_layout(

            fig,

            title=title,

            xaxis_title=x,

            yaxis_title=y
        )

    # ─────────────────────────────────────
    # SCATTER PLOT CONFIG
    # ─────────────────────────────────────

    def create_scatter_plot(

        self,

        df,

        x,

        y,

        color=None,

        size=None,

        title="Scatter Plot"

    ):

        fig = px.scatter(

            df,

            x=x,

            y=y,

            color=color,

            size=size,

            color_discrete_sequence=
            self.color_palette

        )

        return self.apply_layout(

            fig,

            title=title,

            xaxis_title=x,

            yaxis_title=y
        )

    # ─────────────────────────────────────
    # HISTOGRAM CONFIG
    # ─────────────────────────────────────

    def create_histogram(

        self,

        df,

        column,

        color=None,

        bins=30,

        title="Histogram"

    ):

        fig = px.histogram(

            df,

            x=column,

            nbins=bins,

            color=color,

            color_discrete_sequence=
            self.color_palette

        )

        return self.apply_layout(

            fig,

            title=title,

            xaxis_title=column,

            yaxis_title="Count"
        )

    # ─────────────────────────────────────
    # BOX PLOT CONFIG
    # ─────────────────────────────────────

    def create_box_plot(

        self,

        df,

        x=None,

        y=None,

        color=None,

        title="Box Plot"

    ):

        fig = px.box(

            df,

            x=x,

            y=y,

            color=color,

            color_discrete_sequence=
            self.color_palette

        )

        return self.apply_layout(

            fig,

            title=title,

            xaxis_title=x if x else "",

            yaxis_title=y if y else ""
        )

    # ─────────────────────────────────────
    # PIE CHART CONFIG
    # ─────────────────────────────────────

    def create_pie_chart(

        self,

        df,

        names,

        values=None,

        title="Pie Chart"

    ):

        fig = px.pie(

            df,

            names=names,

            values=values,

            color_discrete_sequence=
            self.color_palette

        )

        return self.apply_layout(

            fig,

            title=title
        )

    # ─────────────────────────────────────
    # HEATMAP CONFIG
    # ─────────────────────────────────────

    def create_heatmap(

        self,

        corr_matrix,

        title="Correlation Heatmap"

    ):

        fig = go.Figure(

            data=go.Heatmap(

                z=corr_matrix.values,

                x=corr_matrix.columns,

                y=corr_matrix.columns,

                colorscale="Blues",

                text=corr_matrix.round(2)
                .values,

                texttemplate="%{text}",

                hoverongaps=False
            )
        )

        return self.apply_layout(

            fig,

            title=title
        )

    # ─────────────────────────────────────
    # DASHBOARD METRIC CARD CONFIG
    # ─────────────────────────────────────

    def get_metric_card_style(self):

        return {

            "padding":
                "15px",

            "border_radius":
                "10px",

            "background":
                "#F8FAFC",

            "box_shadow":
                (
                    "0px 2px 5px "
                    "rgba(0,0,0,0.1)"
                ),

            "margin_bottom":
                "10px"
        }

    # ─────────────────────────────────────
    # KPI COLOR CONFIG
    # ─────────────────────────────────────

    def get_quality_color(
        self,
        score
    ):

        if score >= 90:

            return "#16A34A"

        elif score >= 75:

            return "#D97706"

        return "#DC2626"

    # ─────────────────────────────────────
    # EXPORT SETTINGS
    # ─────────────────────────────────────

    def get_export_config(self):

        return self.export_config

    # ─────────────────────────────────────
    # FULL CONFIG EXPORT
    # ─────────────────────────────────────

    def export_config(self):

        return {

            "theme":
                self.theme,

            "color_palette":
                self.color_palette,

            "default_chart_config":
                self.default_chart_config,

            "export_config":
                self.export_config
        }
# core/report_generator.py

import os
from datetime import datetime

from reportlab.platypus import (

    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak

)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter


class ReportGenerator:

    def __init__(self):

        self.output_dir = (
            "outputs/reports"
        )

        os.makedirs(
            self.output_dir,
            exist_ok=True
        )

        self.styles = (
            getSampleStyleSheet()
        )

    # ─────────────────────────────────────
    # GENERATE COMPLETE REPORT
    # ─────────────────────────────────────

    def generate_report(

        self,

        analyzer,
        insights,
        filename="healthcare_report"

    ):

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        filepath = os.path.join(

            self.output_dir,

            f"{filename}_{timestamp}.pdf"
        )

        doc = SimpleDocTemplate(

            filepath,

            pagesize=letter

        )

        elements = []

        # ─────────────────────────────
        # TITLE
        # ─────────────────────────────

        title = Paragraph(

            "Healthcare Analytics Report",

            self.styles["Title"]

        )

        elements.append(title)

        elements.append(
            Spacer(1, 20)
        )

        # ─────────────────────────────
        # REPORT INFO
        # ─────────────────────────────

        generated_time = (
            datetime.now()
            .strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )

        info_text = Paragraph(

            (
                f"<b>Generated:</b> "
                f"{generated_time}"
            ),

            self.styles["Normal"]

        )

        elements.append(info_text)

        elements.append(
            Spacer(1, 20)
        )

        # ─────────────────────────────
        # DATASET OVERVIEW
        # ─────────────────────────────

        overview_title = Paragraph(

            "Dataset Overview",

            self.styles["Heading2"]

        )

        elements.append(
            overview_title
        )

        overview = (
            analyzer
            .get_overview()
        )

        overview_data = [

            ["Metric", "Value"],

            [
                "Total Rows",
                overview["total_rows"]
            ],

            [
                "Total Columns",
                overview["total_columns"]
            ],

            [
                "Numeric Columns",
                overview["numeric_columns"]
            ],

            [
                "Categorical Columns",
                overview[
                    "categorical_columns"
                ]
            ],

            [
                "Missing Values",
                overview[
                    "missing_values"
                ]
            ],

            [
                "Duplicate Rows",
                overview[
                    "duplicate_rows"
                ]
            ],

            [
                "Memory Usage",
                overview[
                    "memory_usage"
                ]
            ]
        ]

        overview_table = Table(
            overview_data,
            colWidths=[220, 220]
        )

        overview_table.setStyle(

            TableStyle([

                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightblue
                ),

                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.black
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.black
                ),

                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, 0),
                    10
                )
            ])
        )

        elements.append(
            overview_table
        )

        elements.append(
            Spacer(1, 20)
        )

        # ─────────────────────────────
        # QUALITY SCORE
        # ─────────────────────────────

        quality_title = Paragraph(

            "Dataset Quality",

            self.styles["Heading2"]

        )

        elements.append(
            quality_title
        )

        quality = (
            analyzer
            .calculate_quality_score()
        )

        quality_text = Paragraph(

            (
                f"<b>Overall Quality Score:</b> "
                f"{quality['overall_score']}/100"
            ),

            self.styles["Normal"]

        )

        elements.append(
            quality_text
        )

        elements.append(
            Spacer(1, 10)
        )

        # ─────────────────────────────
        # HEALTH REPORT
        # ─────────────────────────────

        health = (
            analyzer
            .generate_health_report()
        )

        health_title = Paragraph(

            "Health Report",

            self.styles["Heading2"]

        )

        elements.append(
            health_title
        )

        for issue in health["issues"]:

            issue_paragraph = Paragraph(

                f"• {issue}",

                self.styles["Normal"]

            )

            elements.append(
                issue_paragraph
            )

        elements.append(
            Spacer(1, 20)
        )

        # ─────────────────────────────
        # RECOMMENDATIONS
        # ─────────────────────────────

        recommendation_title = Paragraph(

            "Recommendations",

            self.styles["Heading2"]

        )

        elements.append(
            recommendation_title
        )

        recommendations = (
            analyzer
            .get_recommendations()
        )

        for rec in recommendations:

            rec_paragraph = Paragraph(

                f"• {rec}",

                self.styles["Normal"]

            )

            elements.append(
                rec_paragraph
            )

        elements.append(
            Spacer(1, 20)
        )

        # ─────────────────────────────
        # INSIGHTS SECTION
        # ─────────────────────────────

        insights_title = Paragraph(

            "Generated Insights",

            self.styles["Heading2"]

        )

        elements.append(
            insights_title
        )

        for insight in insights:

            insight_text = (

                f"<b>{insight['title']}</b>: "
                f"{insight['message']}"
            )

            insight_paragraph = Paragraph(

                insight_text,

                self.styles["BodyText"]

            )

            elements.append(
                insight_paragraph
            )

            elements.append(
                Spacer(1, 8)
            )

        elements.append(
            Spacer(1, 20)
        )

        # ─────────────────────────────
        # STATISTICS SECTION
        # ─────────────────────────────

        stats = (
            analyzer
            .get_statistics()
        )

        if not stats.empty:

            stats_title = Paragraph(

                "Statistical Summary",

                self.styles["Heading2"]

            )

            elements.append(
                stats_title
            )

            stats_data = [

                ["Metric"]
                +
                list(stats.columns)
            ]

            for index in stats.index:

                row = [index]

                for value in \
                        stats.loc[index]:

                    row.append(
                        str(value)
                    )

                stats_data.append(row)

            stats_table = Table(
                stats_data
            )

            stats_table.setStyle(

                TableStyle([

                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.lightgrey
                    ),

                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        1,
                        colors.black
                    ),

                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold"
                    ),

                    (
                        "FONTSIZE",
                        (0, 0),
                        (-1, -1),
                        8
                    )
                ])
            )

            elements.append(
                stats_table
            )

        # ─────────────────────────────
        # BUILD PDF
        # ─────────────────────────────

        doc.build(elements)

        return filepath

    # ─────────────────────────────────────
    # GENERATE SIMPLE TEXT REPORT
    # ─────────────────────────────────────

    def generate_text_report(

        self,

        analyzer,
        insights,
        filename="analytics_report"

    ):

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        filepath = os.path.join(

            self.output_dir,

            f"{filename}_{timestamp}.txt"
        )

        with open(

            filepath,

            "w",

            encoding="utf-8"

        ) as file:

            file.write(
                "HEALTHCARE ANALYTICS REPORT\n"
            )

            file.write(
                "=" * 50 + "\n\n"
            )

            overview = (
                analyzer
                .get_overview()
            )

            file.write(
                "DATASET OVERVIEW\n"
            )

            file.write(
                "-" * 30 + "\n"
            )

            for key, value in \
                    overview.items():

                file.write(
                    f"{key}: {value}\n"
                )

            file.write("\n")

            quality = (
                analyzer
                .calculate_quality_score()
            )

            file.write(
                "QUALITY SCORE\n"
            )

            file.write(
                "-" * 30 + "\n"
            )

            file.write(

                f"Overall Score: "
                f"{quality['overall_score']}/100\n\n"
            )

            file.write(
                "INSIGHTS\n"
            )

            file.write(
                "-" * 30 + "\n"
            )

            for insight in insights:

                file.write(

                    f"[{insight['type'].upper()}] "
                    f"{insight['title']}\n"

                )

                file.write(

                    f"{insight['message']}\n\n"

                )

        return filepath

    # ─────────────────────────────────────
    # GET REPORT DIRECTORY
    # ─────────────────────────────────────

    def get_output_directory(self):

        return self.output_dir
# core/export_manager.py

import os
import json
import pandas as pd


class ExportManager:

    def __init__(self):

        self.export_log = []

        self.base_output_dir = "outputs"

        self.export_paths = {

            "reports":
                os.path.join(
                    self.base_output_dir,
                    "reports"
                ),

            "exports":
                os.path.join(
                    self.base_output_dir,
                    "exports"
                ),

            "powerbi":
                os.path.join(
                    self.base_output_dir,
                    "powerbi"
                ),

            "tableau":
                os.path.join(
                    self.base_output_dir,
                    "tableau"
                )
        }

        self._create_output_directories()

    # ─────────────────────────────────────
    # CREATE OUTPUT DIRECTORIES
    # ─────────────────────────────────────

    def _create_output_directories(self):

        for path in self.export_paths.values():

            os.makedirs(
                path,
                exist_ok=True
            )

    # ─────────────────────────────────────
    # EXPORT CSV
    # ─────────────────────────────────────

    def export_csv(
        self,
        df,
        filename,
        export_type="exports"
    ):

        if df.empty:
            raise ValueError(
                "Cannot export empty dataset"
            )

        if export_type \
                not in self.export_paths:

            raise ValueError(
                f"Invalid export type: "
                f"{export_type}"
            )

        filepath = os.path.join(

            self.export_paths[
                export_type
            ],

            f"{filename}.csv"
        )

        df.to_csv(
            filepath,
            index=False
        )

        self.export_log.append(
            f"✅ CSV exported: {filepath}"
        )

        return filepath

    # ─────────────────────────────────────
    # EXPORT JSON
    # ─────────────────────────────────────

    def export_json(
        self,
        data,
        filename,
        export_type="exports"
    ):

        if export_type \
                not in self.export_paths:

            raise ValueError(
                f"Invalid export type: "
                f"{export_type}"
            )

        filepath = os.path.join(

            self.export_paths[
                export_type
            ],

            f"{filename}.json"
        )

        with open(
            filepath,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
                default=str
            )

        self.export_log.append(
            f"✅ JSON exported: {filepath}"
        )

        return filepath

    # ─────────────────────────────────────
    # EXPORT EXCEL
    # ─────────────────────────────────────

    def export_excel(
        self,
        df,
        filename,
        export_type="exports"
    ):

        if df.empty:
            raise ValueError(
                "Cannot export empty dataset"
            )

        filepath = os.path.join(

            self.export_paths[
                export_type
            ],

            f"{filename}.xlsx"
        )

        df.to_excel(
            filepath,
            index=False
        )

        self.export_log.append(
            f"✅ Excel exported: {filepath}"
        )

        return filepath

    # ─────────────────────────────────────
    # EXPORT POWER BI DATASET
    # ─────────────────────────────────────

    def export_powerbi_dataset(
        self,
        df,
        filename="powerbi_ready"
    ):

        filepath = self.export_csv(

            df=df,

            filename=filename,

            export_type="powerbi"
        )

        self.export_log.append(
            "📊 Power BI dataset prepared"
        )

        return filepath

    # ─────────────────────────────────────
    # EXPORT TABLEAU DATASET
    # ─────────────────────────────────────

    def export_tableau_dataset(
        self,
        df,
        filename="tableau_ready"
    ):

        filepath = self.export_csv(

            df=df,

            filename=filename,

            export_type="tableau"
        )

        self.export_log.append(
            "📈 Tableau dataset prepared"
        )

        return filepath

    # ─────────────────────────────────────
    # EXPORT VISUALIZATION CONFIG
    # ─────────────────────────────────────

    def export_visualization_config(
        self,
        config,
        filename="visualization_config"
    ):

        filepath = self.export_json(

            data=config,

            filename=filename,

            export_type="exports"
        )

        self.export_log.append(
            (
                "🎨 Visualization "
                "configuration exported"
            )
        )

        return filepath

    # ─────────────────────────────────────
    # EXPORT ANALYTICS SUMMARY
    # ─────────────────────────────────────

    def export_analytics_summary(
        self,
        summary_data,
        filename="analytics_summary"
    ):

        filepath = self.export_json(

            data=summary_data,

            filename=filename,

            export_type="reports"
        )

        self.export_log.append(
            (
                "🧠 Analytics summary "
                "exported"
            )
        )

        return filepath

    # ─────────────────────────────────────
    # SAVE REPORT TEXT
    # ─────────────────────────────────────

    def save_report_text(
        self,
        text,
        filename="report"
    ):

        filepath = os.path.join(

            self.export_paths[
                "reports"
            ],

            f"{filename}.txt"
        )

        with open(
            filepath,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(text)

        self.export_log.append(
            f"📝 Report saved: {filepath}"
        )

        return filepath

    # ─────────────────────────────────────
    # GET EXPORT LOG
    # ─────────────────────────────────────

    def get_export_log(self):

        return self.export_log

    # ─────────────────────────────────────
    # CLEAR EXPORT LOG
    # ─────────────────────────────────────

    def clear_export_log(self):

        self.export_log = []

    # ─────────────────────────────────────
    # LIST EXPORTED FILES
    # ─────────────────────────────────────

    def list_exported_files(self):

        exported_files = {}

        for key, path in \
                self.export_paths.items():

            files = []

            if os.path.exists(path):

                files = os.listdir(path)

            exported_files[key] = files

        return exported_files

    # ─────────────────────────────────────
    # EXPORT STATUS
    # ─────────────────────────────────────

    def get_export_status(self):

        return {

            "output_directories":
                self.export_paths,

            "total_exports":
                len(self.export_log),

            "recent_exports":
                self.export_log[-5:]
        }
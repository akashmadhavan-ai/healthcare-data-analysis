# core/domain_detector.py

import re


class DomainDetector:

    def __init__(self):

        self.domain_keywords = {

            "healthcare": [

                "patient",
                "diagnosis",
                "disease",
                "hospital",
                "doctor",
                "medical",
                "medicine",
                "treatment",
                "glucose",
                "blood",
                "insulin",
                "pressure",
                "cholesterol",
                "heart",
                "bmi",
                "pregnancies",
                "outcome",
                "diabetes",
                "health",
                "pulse",
                "oxygen",
                "temperature",
                "clinic",
                "symptom",
                "therapy"

            ],

            "finance": [

                "salary",
                "income",
                "loan",
                "interest",
                "credit",
                "debit",
                "transaction",
                "balance",
                "tax",
                "investment",
                "revenue",
                "profit",
                "expense",
                "bank",
                "stock"

            ],

            "education": [

                "student",
                "teacher",
                "course",
                "subject",
                "grade",
                "exam",
                "school",
                "college",
                "attendance",
                "marks",
                "education",
                "assignment",
                "semester"

            ],

            "retail": [

                "product",
                "customer",
                "sales",
                "purchase",
                "inventory",
                "order",
                "shipping",
                "price",
                "retail",
                "store",
                "quantity"

            ],

            "human_resources": [

                "employee",
                "department",
                "salary",
                "experience",
                "joining",
                "attendance",
                "designation",
                "manager",
                "recruitment",
                "performance"

            ]

        }

    # ─────────────────────────────────────
    # CLEAN COLUMN NAMES
    # ─────────────────────────────────────

    def _clean_columns(
        self,
        columns
    ):

        cleaned = []

        for col in columns:

            col = str(col).lower()

            col = re.sub(
                r"[^a-zA-Z0-9_ ]",
                "",
                col
            )

            cleaned.append(col)

        return cleaned

    # ─────────────────────────────────────
    # DETECT DOMAIN
    # ─────────────────────────────────────

    def detect_domain(
        self,
        df
    ):

        columns = self._clean_columns(
            df.columns
        )

        domain_scores = {}

        for domain, keywords in \
                self.domain_keywords.items():

            score = 0

            matched_keywords = []

            for col in columns:

                for keyword in keywords:

                    if keyword in col:

                        score += 1

                        matched_keywords.append(
                            keyword
                        )

            domain_scores[domain] = {

                "score":
                    score,

                "matched_keywords":
                    list(
                        set(
                            matched_keywords
                        )
                    )
            }

        best_domain = max(
            domain_scores,
            key=lambda x:
            domain_scores[x]["score"]
        )

        best_score = \
            domain_scores[
                best_domain
            ]["score"]

        total_columns = len(columns)

        confidence = round(

            min(
                (
                    best_score /
                    max(total_columns, 1)
                ),
                1.0
            ),

            2
        )

        if best_score == 0:

            return {

                "domain":
                    "unknown",

                "confidence":
                    0.0,

                "matched_keywords":
                    [],

                "all_scores":
                    domain_scores
            }

        return {

            "domain":
                best_domain,

            "confidence":
                confidence,

            "matched_keywords":
                domain_scores[
                    best_domain
                ][
                    "matched_keywords"
                ],

            "all_scores":
                domain_scores
        }

    # ─────────────────────────────────────
    # SIMPLE DOMAIN NAME
    # ─────────────────────────────────────

    def get_domain_name(
        self,
        df
    ):

        result = self.detect_domain(df)

        return result["domain"]

    # ─────────────────────────────────────
    # DOMAIN CONFIDENCE
    # ─────────────────────────────────────

    def get_confidence_score(
        self,
        df
    ):

        result = self.detect_domain(df)

        return result["confidence"]

    # ─────────────────────────────────────
    # DOMAIN SUMMARY
    # ─────────────────────────────────────

    def get_domain_summary(
        self,
        df
    ):

        result = self.detect_domain(df)

        return {

            "detected_domain":
                result["domain"],

            "confidence":
                result["confidence"],

            "matched_keywords":
                result[
                    "matched_keywords"
                ],

            "available_domains":
                list(
                    self.domain_keywords
                    .keys()
                )
        }


# ─────────────────────────────────────
# QUICK FUNCTION ACCESS
# ─────────────────────────────────────

def detect_domain(df):

    detector = DomainDetector()

    return detector.detect_domain(df)


def detect_healthcare_domain(df):

    detector = DomainDetector()

    result = detector.detect_domain(df)

    return (
        result["domain"]
        == "healthcare"
    )
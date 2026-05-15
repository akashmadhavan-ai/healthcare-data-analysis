# tests/test_loader.py

import pandas as pd

from core.loader import (
    DataLoader,
    SampleDataLoader
)


# ─────────────────────────────────────
# TEST 1 — SAMPLE DATASET LOADING
# ─────────────────────────────────────

print("\n" + "=" * 50)
print("TEST 1 — SAMPLE DATASET LOADING")
print("=" * 50)

try:
    df = SampleDataLoader.load_sample_dataset(
        "diabetes"
    )

    print("✅ Diabetes sample loaded")

    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nPreview:")
    print(df.head())

except Exception as e:
    print(f"❌ Failed: {e}")


# ─────────────────────────────────────
# TEST 2 — DATASET PROFILING
# ─────────────────────────────────────

print("\n" + "=" * 50)
print("TEST 2 — DATASET PROFILING")
print("=" * 50)

try:
    loader = DataLoader()

    loader.raw_df = df

    info = loader._build_dataset_info(df)

    print("✅ Dataset profiling success")

    print(f"\nRows: {info['rows']}")
    print(f"Columns: {info['columns']}")

    print(f"\nDomain: {info['domain']}")
    print(
        f"Confidence: "
        f"{info['domain_confidence']:.2f}"
    )

    print(
        f"\nMissing Values: "
        f"{info['missing_count']}"
    )

    print(
        f"Duplicate Rows: "
        f"{info['duplicate_count']}"
    )

    print(
        f"Memory Usage: "
        f"{info['memory_usage']}"
    )

except Exception as e:
    print(f"❌ Failed: {e}")


# ─────────────────────────────────────
# TEST 3 — COLUMN SUMMARY
# ─────────────────────────────────────

print("\n" + "=" * 50)
print("TEST 3 — COLUMN SUMMARY")
print("=" * 50)

try:
    summary = loader.get_column_summary()

    print("✅ Column summary generated")

    print("\nSummary Preview:")
    print(summary.head())

except Exception as e:
    print(f"❌ Failed: {e}")


# ─────────────────────────────────────
# TEST 4 — NUMERIC / CATEGORICAL
# ─────────────────────────────────────

print("\n" + "=" * 50)
print("TEST 4 — COLUMN TYPE CHECK")
print("=" * 50)

try:
    info = loader._build_dataset_info(df)

    print("✅ Column type detection success")

    print("\nNumeric Columns:")
    print(info["numeric_columns"])

    print("\nCategorical Columns:")
    print(info["categorical_columns"])

    print("\nBinary Columns:")
    print(info["binary_columns"])

except Exception as e:
    print(f"❌ Failed: {e}")


# ─────────────────────────────────────
# TEST 5 — MISSING VALUES
# ─────────────────────────────────────

print("\n" + "=" * 50)
print("TEST 5 — MISSING VALUE ANALYSIS")
print("=" * 50)

try:
    missing = df.isna().sum()

    print("✅ Missing value analysis success")

    print("\nMissing Values Per Column:")
    print(missing)

except Exception as e:
    print(f"❌ Failed: {e}")


# ─────────────────────────────────────
# TEST 6 — DATA PREVIEW
# ─────────────────────────────────────

print("\n" + "=" * 50)
print("TEST 6 — DATA PREVIEW")
print("=" * 50)

try:
    preview = loader.get_sample(10)

    print("✅ Data preview success")

    print("\nFirst 10 Rows:")
    print(preview)

except Exception as e:
    print(f"❌ Failed: {e}")


# ─────────────────────────────────────
# FINAL STATUS
# ─────────────────────────────────────

print("\n" + "=" * 50)
print("ALL LOADER TESTS COMPLETED")
print("=" * 50)
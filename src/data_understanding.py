"""Utilities for the Home Credit Default Risk data-understanding phase."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Literal, Mapping

import pandas as pd

EXPECTED_FILES: Mapping[str, str] = {
    "application_train": "application_train.csv",
    "application_test": "application_test.csv",
    "bureau": "bureau.csv",
    "bureau_balance": "bureau_balance.csv",
    "previous_application": "previous_application.csv",
    "installments_payments": "installments_payments.csv",
    "credit_card_balance": "credit_card_balance.csv",
    "pos_cash_balance": "POS_CASH_balance.csv",
}


def resolve_data_dir(
    preferred: Path | str | None = None,
    *,
    candidates: Iterable[Path | str] | None = None,
) -> Path:
    """
    Pick a directory that contains competition CSV files.

    If ``preferred`` exists and contains at least one expected CSV, it wins.
    Otherwise the first candidate directory that contains ``application_train.csv`` is used.
    """

    def _has_train_csv(d: Path) -> bool:
        return (d / EXPECTED_FILES["application_train"]).is_file()

    if preferred is not None:
        p = Path(preferred).expanduser().resolve()
        if p.is_dir() and _has_train_csv(p):
            return p

    defaults = [
        Path("data") / "raw",
        Path("data"),
        Path("."),
    ]
    for raw in candidates or defaults:
        d = Path(raw).expanduser().resolve()
        if d.is_dir() and _has_train_csv(d):
            return d

    raise FileNotFoundError(
        "Could not locate CSV directory containing application_train.csv. "
        "Pass resolve_data_dir(preferred='/path/to/your/kaggle/files')."
    )


def scan_csv_paths(data_dir: Path | str) -> dict[str, Path]:
    """Map logical table names to existing CSV paths under ``data_dir``."""
    root = Path(data_dir).expanduser().resolve()
    found: dict[str, Path] = {}
    for key, fname in EXPECTED_FILES.items():
        path = root / fname
        if path.is_file():
            found[key] = path
    return found


def file_size_mb(path: Path) -> float:
    return path.stat().st_size / (1024 * 1024)


def count_rows_chunked(path: Path, chunksize: int = 500_000) -> int:
    total = 0
    reader = pd.read_csv(path, chunksize=chunksize, low_memory=False)
    for chunk in reader:
        total += len(chunk)
    return total


def dtypes_and_columns(path: Path, nrows: int = 5000) -> pd.DataFrame:
    """Infer dtypes from the first rows (``low_memory=False`` stabilizes dtypes)."""
    sample = pd.read_csv(path, nrows=nrows, low_memory=False)
    info = pd.DataFrame(
        {
            "dtype": sample.dtypes.astype(str),
            "non_null_first_nrows": sample.notna().sum(),
        }
    )
    info.index.name = "column"
    return info.reset_index()


def missing_rate_chunked(path: Path, chunksize: int = 300_000) -> tuple[int, pd.DataFrame]:
    """Full-file missing counts via chunked reads (memory-safe for large CSVs)."""
    na_totals: pd.Series | None = None
    row_total = 0
    reader = pd.read_csv(path, chunksize=chunksize, low_memory=False)
    for chunk in reader:
        row_total += len(chunk)
        chunk_na = chunk.isna().sum()
        na_totals = chunk_na if na_totals is None else na_totals.add(chunk_na, fill_value=0)

    if na_totals is None or row_total == 0:
        return row_total, pd.DataFrame(columns=["column", "missing_count", "missing_pct"])

    out = (
        pd.DataFrame({"missing_count": na_totals})
        .assign(missing_pct=lambda d: d["missing_count"] / row_total * 100)
        .sort_values("missing_pct", ascending=False)
        .reset_index()
        .rename(columns={"index": "column"})
    )
    return row_total, out


def missing_rate_sample(path: Path, nrows: int = 100_000) -> tuple[int, pd.DataFrame]:
    """Approximate missing rates using only the first ``nrows`` rows (fast)."""
    df = pd.read_csv(path, nrows=nrows, low_memory=False)
    row_total = len(df)
    if row_total == 0:
        return 0, pd.DataFrame(columns=["column", "missing_count", "missing_pct"])

    na_totals = df.isna().sum()
    out = (
        pd.DataFrame({"missing_count": na_totals})
        .assign(missing_pct=lambda d: d["missing_count"] / row_total * 100)
        .sort_values("missing_pct", ascending=False)
        .reset_index()
        .rename(columns={"index": "column"})
    )
    return row_total, out


def numeric_ranges_sample(path: Path, nrows: int = 50_000) -> pd.DataFrame:
    """Min / max / mean on numeric columns using a prefix sample (fast exploratory view)."""
    df = pd.read_csv(path, nrows=nrows, low_memory=False)
    num = df.select_dtypes(include=["number"])
    if num.empty:
        return pd.DataFrame()
    desc = num.agg(["min", "max", "mean"]).T
    desc.index.name = "column"
    return desc.reset_index()


def summarize_csv(
    path: Path,
    *,
    chunksize: int = 300_000,
    missing: Literal["sample", "full"] = "sample",
    sample_rows: int = 100_000,
    top_missing_n: int = 15,
) -> dict[str, object]:
    """Disk size, row/column counts, and highest missing-rate columns."""
    size_mb = round(file_size_mb(path), 2)
    cols = len(pd.read_csv(path, nrows=0).columns)
    rows = count_rows_chunked(path, chunksize=chunksize)

    if missing == "full":
        _, missing_df = missing_rate_chunked(path, chunksize=chunksize)
    else:
        _, missing_df = missing_rate_sample(path, nrows=sample_rows)

    return {
        "path": path,
        "size_mb": size_mb,
        "rows": rows,
        "cols": cols,
        "missing_mode": missing,
        "top_missing": missing_df.head(top_missing_n),
    }


def application_train_specials(train_path: Path) -> None:
    """Print TARGET balance and duplicate ``SK_ID_CURR`` counts."""
    df = pd.read_csv(train_path, usecols=["TARGET", "SK_ID_CURR"], low_memory=False)
    vc = df["TARGET"].value_counts(dropna=False).sort_index()
    print("TARGET distribution:")
    print(vc.to_string())
    print(f"\nPositive rate (TARGET==1): {df['TARGET'].mean():.4f}")

    dup = df["SK_ID_CURR"].duplicated().sum()
    print(f"\nDuplicate SK_ID_CURR rows: {dup}")

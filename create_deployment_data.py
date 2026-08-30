import pandas as pd
from pathlib import Path

# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "sales_transactions_cleaned.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "deployment"
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("CREATING DEPLOYMENT DATA")
print("=" * 60)

print("\nInput file:")
print(INPUT_FILE)

# ============================================================
# COLUMNS REQUIRED BY SALES ANALYTICS
# ============================================================

USE_COLUMNS = [
    "date",
    "receipt_id",
    "store_id",
    "sku_id",
    "quantity",
    "total_value",
    "channel"
]

# ============================================================
# READ LARGE CSV IN CHUNKS
# ============================================================

print("\nReading large dataset in chunks...")

chunks = []

for chunk in pd.read_csv(
    INPUT_FILE,
    usecols=USE_COLUMNS,
    parse_dates=["date"],
    chunksize=250_000
):
    chunks.append(chunk)

    print(f"Loaded chunk: {len(chunk):,} rows")

df = pd.concat(chunks, ignore_index=True)

print(f"\nTotal rows loaded: {len(df):,}")

# ============================================================
# CLEAN BASIC TYPES
# ============================================================

df["date"] = pd.to_datetime(
    df["date"],
    errors="coerce"
)

df["quantity"] = pd.to_numeric(
    df["quantity"],
    errors="coerce"
).fillna(0)

df["total_value"] = pd.to_numeric(
    df["total_value"],
    errors="coerce"
).fillna(0)

df = df.dropna(subset=["date"])

df["year"] = df["date"].dt.year

# ============================================================
# CREATE DAILY SALES DATA
# ============================================================

print("\nCreating daily sales summary...")

daily_sales = (
    df.groupby(
        ["date", "year", "channel"],
        as_index=False
    )
    .agg(
        total_value=("total_value", "sum"),
        quantity=("quantity", "sum"),
        transactions=("receipt_id", "nunique"),
        active_stores=("store_id", "nunique"),
        active_products=("sku_id", "nunique")
    )
)

daily_file = OUTPUT_DIR / "daily_sales_dashboard.csv"

daily_sales.to_csv(
    daily_file,
    index=False
)

print(f"Saved: {daily_file}")

# ============================================================
# CREATE STORE SALES DATA
# ============================================================

print("\nCreating store sales summary...")

store_sales = (
    df.groupby(
        ["year", "channel", "store_id"],
        as_index=False
    )
    .agg(
        total_value=("total_value", "sum"),
        quantity=("quantity", "sum"),
        transactions=("receipt_id", "nunique")
    )
)

store_file = OUTPUT_DIR / "store_sales_dashboard.csv"

store_sales.to_csv(
    store_file,
    index=False
)

print(f"Saved: {store_file}")

# ============================================================
# CREATE CHANNEL SALES DATA
# ============================================================

print("\nCreating channel sales summary...")

channel_sales = (
    df.groupby(
        ["year", "channel"],
        as_index=False
    )
    .agg(
        total_value=("total_value", "sum"),
        quantity=("quantity", "sum"),
        transactions=("receipt_id", "nunique"),
        active_stores=("store_id", "nunique"),
        active_products=("sku_id", "nunique")
    )
)

channel_file = OUTPUT_DIR / "channel_sales_dashboard.csv"

channel_sales.to_csv(
    channel_file,
    index=False
)

print(f"Saved: {channel_file}")

# ============================================================
# CREATE YEARLY SALES DATA
# ============================================================

print("\nCreating yearly sales summary...")

yearly_sales = (
    df.groupby(
        ["year"],
        as_index=False
    )
    .agg(
        total_value=("total_value", "sum"),
        quantity=("quantity", "sum"),
        transactions=("receipt_id", "nunique"),
        active_stores=("store_id", "nunique"),
        active_products=("sku_id", "nunique")
    )
)

year_file = OUTPUT_DIR / "yearly_sales_dashboard.csv"

yearly_sales.to_csv(
    year_file,
    index=False
)

print(f"Saved: {year_file}")

# ============================================================
# FINAL INFORMATION
# ============================================================

print("\n" + "=" * 60)
print("DEPLOYMENT DATA CREATED SUCCESSFULLY")
print("=" * 60)

print("\nFiles created:")

for file in OUTPUT_DIR.glob("*.csv"):
    size_mb = file.stat().st_size / (1024 * 1024)

    print(
        f"{file.name:<35} "
        f"{size_mb:.2f} MB"
    )

print("\nYour original 902 MB dataset was NOT modified.")
print("Your notebooks were NOT modified.")
"""
scripts/data_preparation/prepare_sales_data.py

This script reads data from the data/raw folder, cleans the data,
and writes the cleaned version to the data/prepared folder.

Tasks:
- Remove duplicates
- Handle missing values
- Remove outliers
- Ensure consistent formatting


# Terminal command to run this file from the root project folder:
uv run python -m analytics_project.data_preparation.prepare_sales_data
"""
#####################################
# Import Modules at the Top
#####################################

import pathlib
import sys

import pandas as pd

# Ensure project root is in sys.path for local imports
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent.parent))

from utils.logger import logger  # noqa: E402

# Constants
SCRIPTS_DATA_PREP_DIR: pathlib.Path = pathlib.Path(__file__).resolve().parent
PROJECT_ROOT: pathlib.Path = pathlib.Path(__file__).resolve().parents[3]

SCRIPTS_DIR: pathlib.Path = PROJECT_ROOT / "src" / "analytics_project"

DATA_DIR: pathlib.Path = PROJECT_ROOT / "data"
RAW_DATA_DIR: pathlib.Path = DATA_DIR / "raw"
PREPARED_DATA_DIR: pathlib.Path = DATA_DIR / "prepared"


DATA_DIR.mkdir(exist_ok=True)
RAW_DATA_DIR.mkdir(exist_ok=True)
PREPARED_DATA_DIR.mkdir(exist_ok=True)


#####################################
# Data Preparation Functions
#####################################


def read_raw_data(file_name: str) -> pd.DataFrame:
    """
    Read raw data from CSV.
    """
    logger.info(f"FUNCTION START: read_raw_data with file_name={file_name}")

    file_path = RAW_DATA_DIR.joinpath(file_name)

    logger.info(f"Reading data from {file_path}")

    df = pd.read_csv(file_path)

    logger.info(f"Loaded dataframe with {len(df)} rows and {len(df.columns)} columns")

    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate rows.
    """
    logger.info(f"FUNCTION START: remove_duplicates with dataframe shape={df.shape}")

    initial_count = len(df)

    df = df.drop_duplicates()

    removed_count = initial_count - len(df)

    logger.info(f"Removed {removed_count} duplicate rows")
    logger.info(f"{len(df)} records remaining after removing duplicates.")

    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle missing values.
    """
    logger.info(
        f"FUNCTION START: handle_missing_values with dataframe shape={df.shape}"
    )

    missing_before = df.isna().sum()

    logger.info(f"Missing values before handling:\n{missing_before}")

    # Add business rules here if required

    missing_after = df.isna().sum()

    logger.info(f"Missing values after handling:\n{missing_after}")

    return df


def remove_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove outliers.
    """
    logger.info(f"FUNCTION START: remove_outliers with dataframe shape={df.shape}")

    initial_count = len(df)

    # Add outlier rules here if required

    removed_count = initial_count - len(df)

    logger.info(f"Removed {removed_count} outlier rows")

    return df


def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate data against business rules.
    """
    logger.info(f"FUNCTION START: validate_data with dataframe shape={df.shape}")

    if "SaleAmount" in df.columns:
        df["SaleAmount"] = pd.to_numeric(df["SaleAmount"], errors="coerce")

        invalid_sales = df[df["SaleAmount"] < 0]

        logger.info(f"Found {len(invalid_sales)} records with negative SaleAmount")

        df = df[(df["SaleAmount"] >= 0) | (df["SaleAmount"].isna())]

    logger.info("Data validation complete")

    return df


def standardize_formats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize sales data formats.
    """
    logger.info(f"FUNCTION START: standardize_formats with dataframe shape={df.shape}")

    if "SaleDate" in df.columns:
        df["SaleDate"] = pd.to_datetime(df["SaleDate"])

    if "PaymentType" in df.columns:
        df["PaymentType"] = df["PaymentType"].str.strip().str.title()

    if "SaleAmount" in df.columns:
        df["SaleAmount"] = pd.to_numeric(df["SaleAmount"], errors="coerce").round(2)

    logger.info("Completed standardizing formats")

    return df


def save_prepared_data(df: pd.DataFrame, file_name: str) -> None:
    """
    Save cleaned data to CSV.
    """
    logger.info(
        f"FUNCTION START: save_prepared_data with file_name={file_name}, dataframe shape={df.shape}"
    )

    file_path = PREPARED_DATA_DIR.joinpath(file_name)

    df.to_csv(file_path, index=False)

    logger.info(f"Data saved to {file_path}")
    #####################################


# Define Main Function
#####################################


def main() -> None:
    """
    Main function for processing data.
    """

    logger.info("==================================")
    logger.info("STARTING prepare_sales_data.py")
    logger.info("==================================")

    logger.info(f"Root         : {PROJECT_ROOT}")
    logger.info(f"data/raw     : {RAW_DATA_DIR}")
    logger.info(f"data/prepared: {PREPARED_DATA_DIR}")
    logger.info(f"scripts      : {SCRIPTS_DIR}")

    input_file = "sales_data.csv"
    output_file = "sales_prepared.csv"

    # Read raw data
    df = read_raw_data(input_file)

    # Record original shape
    original_shape = df.shape

    # Log initial dataframe information
    logger.info(f"Initial dataframe columns: {', '.join(df.columns.tolist())}")
    logger.info(f"Initial dataframe shape: {df.shape}")

    # Clean column names
    original_columns = df.columns.tolist()

    df.columns = df.columns.str.strip()

    changed_columns = [
        f"{old} -> {new}"
        for old, new in zip(original_columns, df.columns, strict=True)
        if old != new
    ]

    if changed_columns:
        logger.info(f"Cleaned column names: {', '.join(changed_columns)}")

    # Remove duplicates
    df = remove_duplicates(df)

    # Handle missing values
    df = handle_missing_values(df)

    # Remove outliers
    df = remove_outliers(df)

    # Validate data
    df = validate_data(df)

    # Standardize formats
    df = standardize_formats(df)

    # Save prepared data
    save_prepared_data(df, output_file)

    logger.info("==================================")
    logger.info(f"Original shape: {original_shape}")
    logger.info(f"Cleaned shape:  {df.shape}")
    logger.info("==================================")
    logger.info("FINISHED prepare_sales_data.py")
    logger.info("==================================")


#####################################
# Conditional Execution Block
#####################################


if __name__ == "__main__":
    main()

"""
scripts/data_preparation/prepare_customers_data.py

This script reads customer data from the data/raw folder, cleans the data,
and writes the cleaned version to the data/prepared folder.

Tasks:
- Remove duplicates
- Handle missing values
- Remove outliers
- Ensure consistent formatting

"""

#####################################
# Import Modules at the Top
#####################################

# Import from Python Standard Library
import pathlib
import sys

# Import from external packages (requires a virtual environment)
import pandas as pd

# Ensure project root is in sys.path for local imports
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent.parent))

# Import local modules (e.g. utils/logger.py)
from utils.logger import logger


# Constants
SCRIPTS_DATA_PREP_DIR: pathlib.Path = pathlib.Path(__file__).resolve().parent
PROJECT_ROOT: pathlib.Path = pathlib.Path(__file__).resolve().parents[3]

SCRIPTS_DIR: pathlib.Path = PROJECT_ROOT / "src" / "analytics_project"

DATA_DIR: pathlib.Path = PROJECT_ROOT / "data"
RAW_DATA_DIR: pathlib.Path = DATA_DIR / "raw"
PREPARED_DATA_DIR: pathlib.Path = DATA_DIR / "prepared"


# Ensure the directories exist or create them
DATA_DIR.mkdir(exist_ok=True)
RAW_DATA_DIR.mkdir(exist_ok=True)
PREPARED_DATA_DIR.mkdir(exist_ok=True)


#####################################
# Define Functions - Reusable blocks of code
#####################################


def read_raw_data(file_name: str) -> pd.DataFrame:
    """
    Read raw customer data from CSV.

    Args:
        file_name (str): Name of the CSV file to read.

    Returns:
        pd.DataFrame: Loaded DataFrame.
    """

    logger.info(f"FUNCTION START: read_raw_data with file_name={file_name}")

    file_path = RAW_DATA_DIR.joinpath(file_name)

    logger.info(f"Reading data from {file_path}")

    df = pd.read_csv(file_path)

    logger.info(
        f"Loaded dataframe with {len(df)} rows and {len(df.columns)} columns"
    )

    return df


def save_prepared_data(df: pd.DataFrame, file_name: str) -> None:
    """
    Save cleaned customer data to CSV.

    Args:
        df (pd.DataFrame): Cleaned DataFrame.
        file_name (str): Name of output file.
    """

    logger.info(
        f"FUNCTION START: save_prepared_data with file_name={file_name}, dataframe shape={df.shape}"
    )

    file_path = PREPARED_DATA_DIR.joinpath(file_name)

    df.to_csv(file_path, index=False)

    logger.info(f"Data saved to {file_path}")


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate customer records.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: DataFrame with duplicates removed.
    """

    logger.info(
        f"FUNCTION START: remove_duplicates with dataframe shape={df.shape}"
    )

    initial_count = len(df)

    # TODO: Consider using CustomerID if available
    # Example:
    # df = df.drop_duplicates(subset=["customer_id"])

    df = df.drop_duplicates()

    removed_count = initial_count - len(df)

    logger.info(f"Removed {removed_count} duplicate rows")
    logger.info(f"{len(df)} records remaining after removing duplicates.")

    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle missing values in customer data.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: DataFrame with missing values handled.
    """

    logger.info(
        f"FUNCTION START: handle_missing_values with dataframe shape={df.shape}"
    )

    missing_before = df.isna().sum()

    logger.info(
        f"Missing values by column before handling:\n{missing_before}"
    )

    # TODO: Add customer-specific missing value handling rules
    #
    # Examples:
    # df["customer_name"].fillna("Unknown", inplace=True)
    # df.dropna(subset=["customer_id"], inplace=True)

    missing_after = df.isna().sum()

    logger.info(
        f"Missing values by column after handling:\n{missing_after}"
    )

    logger.info(
        f"{len(df)} records remaining after handling missing values."
    )

    return df


def remove_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove customer data outliers based on business rules.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: DataFrame with outliers removed.
    """

    logger.info(
        f"FUNCTION START: remove_outliers with dataframe shape={df.shape}"
    )

    initial_count = len(df)

    # TODO: Add customer-specific outlier rules
    #
    # Example:
    # if "age" in df.columns:
    #     df = df[(df["age"] >= 0) & (df["age"] <= 120)]

    removed_count = initial_count - len(df)

    logger.info(f"Removed {removed_count} outlier rows")
    logger.info(f"{len(df)} records remaining after removing outliers.")

    return df


def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate customer data against business rules.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: Validated DataFrame.
    """

    logger.info(
        f"FUNCTION START: validate_data with dataframe shape={df.shape}"
    )

    # TODO: Add validation rules specific to customer data
    #
    # Examples:
    # - Validate customer IDs
    # - Check email formatting
    # - Validate dates
    # - Remove invalid records

    logger.info("Data validation complete")

    return df


def standardize_formats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize customer data formats.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: DataFrame with standardized formats.
    """

    logger.info(
        f"FUNCTION START: standardize_formats with dataframe shape={df.shape}"
    )

    # TODO: Add customer formatting rules
    #
    # Examples:
    # df["customer_name"] = df["customer_name"].str.title()
    # df["email"] = df["email"].str.lower()
    # df["phone"] = df["phone"].str.strip()

    logger.info("Completed standardizing formats")

    return df


#####################################
# Define Main Function
#####################################


def main() -> None:
    """
    Main function for processing customer data.
    """

    logger.info("==================================")
    logger.info("STARTING prepare_customers_data.py")
    logger.info("==================================")

    logger.info(f"Root         : {PROJECT_ROOT}")
    logger.info(f"data/raw     : {RAW_DATA_DIR}")
    logger.info(f"data/prepared: {PREPARED_DATA_DIR}")
    logger.info(f"scripts      : {SCRIPTS_DIR}")

    input_file = "customers_data.csv"
    output_file = "customers_prepared.csv"


    # Read raw data
    df = read_raw_data(input_file)


    # Record original shape
    original_shape = df.shape


    # Log initial dataframe information
    logger.info(
        f"Initial dataframe columns: {', '.join(df.columns.tolist())}"
    )
    logger.info(f"Initial dataframe shape: {df.shape}")


    # Clean column names
    original_columns = df.columns.tolist()

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )


    changed_columns = [
        f"{old} -> {new}"
        for old, new in zip(
            original_columns,
            df.columns,
            strict=True
        )
        if old != new
    ]


    if changed_columns:
        logger.info(
            f"Cleaned column names: {', '.join(changed_columns)}"
        )


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
    logger.info("FINISHED prepare_customers_data.py")
    logger.info("==================================")


#####################################
# Conditional Execution Block
#####################################

if __name__ == "__main__":
    main()

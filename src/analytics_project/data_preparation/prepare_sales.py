"""
scripts/data_preparation/prepare_sales.py

This script reads data from the data/raw folder, cleans the data,
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

import pathlib
import sys

import pandas as pd

# Ensure project root is available for local imports
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent.parent))

from utils.logger import logger


#####################################
# Constants
#####################################

SCRIPTS_DATA_PREP_DIR = pathlib.Path(__file__).resolve().parent
SCRIPTS_DIR = SCRIPTS_DATA_PREP_DIR.parent
PROJECT_ROOT = SCRIPTS_DIR.parent

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PREPARED_DATA_DIR = DATA_DIR / "prepared"

DATA_DIR.mkdir(exist_ok=True)
RAW_DATA_DIR.mkdir(exist_ok=True)
PREPARED_DATA_DIR.mkdir(exist_ok=True)


#####################################
# Functions
#####################################

def read_raw_data(file_name: str) -> pd.DataFrame:
    """
    Read raw data from a CSV file.
    """
    logger.info("FUNCTION START: read_raw_data")

    file_path = RAW_DATA_DIR / file_name
    logger.info(f"Reading data from {file_path}")

    df = pd.read_csv(file_path)

    logger.info(
        f"Loaded dataframe with {len(df)} rows and {len(df.columns)} columns"
    )

    logger.info(f"\nColumn types:\n{df.dtypes}")
    logger.info(f"\nUnique values:\n{df.nunique()}")

    return df


def remove_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove outliers from numeric columns using the IQR method.
    """
    numeric_columns = df.select_dtypes(include="number").columns

    cleaned_df = df.copy()

    for column in numeric_columns:
        q1 = cleaned_df[column].quantile(0.25)
        q3 = cleaned_df[column].quantile(0.75)
        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        cleaned_df = cleaned_df[
            (cleaned_df[column] >= lower)
            & (cleaned_df[column] <= upper)
        ]

    return cleaned_df


def save_prepared_data(df: pd.DataFrame, file_name: str) -> None:
    """
    Save the cleaned dataframe.
    """
    output_path = PREPARED_DATA_DIR / file_name
    df.to_csv(output_path, index=False)
    logger.info(f"Prepared data saved to {output_path}")


#####################################
# Main Function
#####################################

def main() -> None:
    """
    Main function for preparing the sales dataset.
    """
    logger.info("==================================")
    logger.info("STARTING prepare_sales.py")
    logger.info("==================================")

    logger.info(f"Project root : {PROJECT_ROOT}")
    logger.info(f"Raw data     : {RAW_DATA_DIR}")
    logger.info(f"Prepared data: {PREPARED_DATA_DIR}")

    input_file = "sales_data.csv"
    output_file = "sales_prepared.csv"

    df = read_raw_data(input_file)

    original_shape = df.shape

    logger.info(f"Initial shape: {original_shape}")
    logger.info(f"Columns: {', '.join(df.columns)}")

    # Clean column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    logger.info(f"Updated columns: {', '.join(df.columns)}")

    # Remove duplicates
    before = len(df)
    df = df.drop_duplicates()
    logger.info(f"Removed {before - len(df)} duplicate rows.")

    # Handle missing values
    numeric_columns = df.select_dtypes(include="number").columns
    categorical_columns = df.select_dtypes(exclude="number").columns

    for column in numeric_columns:
        df[column] = df[column].fillna(df[column].median())

    for column in categorical_columns:
        if not df[column].mode().empty:
            df[column] = df[column].fillna(df[column].mode()[0])

    logger.info("Missing values handled.")

    # Remove outliers
    before = len(df)
    df = remove_outliers(df)
    logger.info(f"Removed {before - len(df)} outlier rows.")

    # Save cleaned data
    save_prepared_data(df, output_file)

    logger.info("==================================")
    logger.info(f"Original shape: {original_shape}")
    logger.info(f"Cleaned shape : {df.shape}")
    logger.info("FINISHED prepare_sales.py")
    logger.info("==================================")


#####################################
# Entry Point
#####################################

if __name__ == "__main__":
    main()
    # Clean column names
    original_columns = df.columns.tolist()
    df.columns = df.columns.str.strip()
    
    # Log if any column names changed
    changed_columns = [f"{old} -> {new}" for old, new in zip(original_columns, df.columns) if old != new]
    if changed_columns:
        logger.info(f"Cleaned column names: {', '.join(changed_columns)}")

    # Remove duplicate rows
    rows_before = len(df)
    df = df.drop_duplicates()
    rows_removed = rows_before - len(df)
    logger.info(f"Removed {rows_removed} duplicate rows.")

    # Handle missing values
    logger.info("Missing values before cleaning:")
    logger.info(f"\n{df.isnull().sum()}")

    # Fill numeric columns with the median
    numeric_cols = df.select_dtypes(include="number").columns
    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].median())

    # Fill categorical columns with the mode
    categorical_cols = df.select_dtypes(exclude="number").columns
    for col in categorical_cols:
        if not df[col].mode().empty:
            df[col] = df[col].fillna(df[col].mode()[0])

    logger.info("Missing values after cleaning:")
    logger.info(f"\n{df.isnull().sum()}")

    # Remove outliers using the IQR method
    rows_before = len(df)

    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        df = df[(df[col] >= lower) & (df[col] <= upper)]

    logger.info(f"Removed {rows_before - len(df)} rows containing outliers.")

    # Save prepared data
    output_path = PREPARED_DATA_DIR / output_file
    df.to_csv(output_path, index=False)
    logger.info(f"Prepared data saved to {output_path}")
    

    logger.info("==================================")
    logger.info(f"Cleaned shape:  {original_shape}")
    logger.info(f"Original shape: {df.shape}")
    logger.info("==================================")
    logger.info("FINISHED prepare_sales_data.py")
    logger.info("==================================")

#####################################
# Conditional Execution Block 
# Ensures the script runs only when executed directly
# This is a common Python convention.
#####################################
"""
scripts/data_preparation/prepare_sales.py

This script reads data from the data/raw folder, cleans the data,
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

import pathlib
import sys

import pandas as pd

# Ensure project root is available for local imports
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent.parent))

from utils.logger import logger


#####################################
# Constants
#####################################

SCRIPTS_DATA_PREP_DIR = pathlib.Path(__file__).resolve().parent
SCRIPTS_DIR = SCRIPTS_DATA_PREP_DIR.parent
PROJECT_ROOT = SCRIPTS_DIR.parent

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PREPARED_DATA_DIR = DATA_DIR / "prepared"

DATA_DIR.mkdir(exist_ok=True)
RAW_DATA_DIR.mkdir(exist_ok=True)
PREPARED_DATA_DIR.mkdir(exist_ok=True)


#####################################
# Functions
#####################################

def read_raw_data(file_name: str) -> pd.DataFrame:
    """
    Read raw data from a CSV file.
    """
    logger.info("FUNCTION START: read_raw_data")

    file_path = RAW_DATA_DIR / file_name
    logger.info(f"Reading data from {file_path}")

    df = pd.read_csv(file_path)

    logger.info(
        f"Loaded dataframe with {len(df)} rows and {len(df.columns)} columns"
    )

    logger.info(f"\nColumn types:\n{df.dtypes}")
    logger.info(f"\nUnique values:\n{df.nunique()}")

    return df


def remove_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove outliers from numeric columns using the IQR method.
    """
    numeric_columns = df.select_dtypes(include="number").columns

    cleaned_df = df.copy()

    for column in numeric_columns:
        q1 = cleaned_df[column].quantile(0.25)
        q3 = cleaned_df[column].quantile(0.75)
        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        cleaned_df = cleaned_df[
            (cleaned_df[column] >= lower)
            & (cleaned_df[column] <= upper)
        ]

    return cleaned_df


def save_prepared_data(df: pd.DataFrame, file_name: str) -> None:
    """
    Save the cleaned dataframe.
    """
    output_path = PREPARED_DATA_DIR / file_name
    df.to_csv(output_path, index=False)
    logger.info(f"Prepared data saved to {output_path}")


#####################################
# Main Function
#####################################

def main() -> None:
    """
    Main function for preparing the sales dataset.
    """
    logger.info("==================================")
    logger.info("STARTING prepare_sales.py")
    logger.info("==================================")

    logger.info(f"Project root : {PROJECT_ROOT}")
    logger.info(f"Raw data     : {RAW_DATA_DIR}")
    logger.info(f"Prepared data: {PREPARED_DATA_DIR}")

    input_file = "sales_data.csv"
    output_file = "sales_prepared.csv"

    df = read_raw_data(input_file)

    original_shape = df.shape

    logger.info(f"Initial shape: {original_shape}")
    logger.info(f"Columns: {', '.join(df.columns)}")

    # Clean column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    logger.info(f"Updated columns: {', '.join(df.columns)}")

    # Remove duplicates
    before = len(df)
    df = df.drop_duplicates()
    logger.info(f"Removed {before - len(df)} duplicate rows.")

    # Handle missing values
    numeric_columns = df.select_dtypes(include="number").columns
    categorical_columns = df.select_dtypes(exclude="number").columns

    for column in numeric_columns:
        df[column] = df[column].fillna(df[column].median())

    for column in categorical_columns:
        if not df[column].mode().empty:
            df[column] = df[column].fillna(df[column].mode()[0])

    logger.info("Missing values handled.")

    # Remove outliers
    before = len(df)
    df = remove_outliers(df)
    logger.info(f"Removed {before - len(df)} outlier rows.")

    # Save cleaned data
    save_prepared_data(df, output_file)

    logger.info("==================================")
    logger.info(f"Original shape: {original_shape}")
    logger.info(f"Cleaned shape : {df.shape}")
    logger.info("FINISHED prepare_sales.py")
    logger.info("==================================")


#####################################
# Entry Point
#####################################

if __name__ == "__main__":
    main()

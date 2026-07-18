"""
data_prep_hospital.py

Hospital Appointment Data Preparation Project.

This project demonstrates cleaning and preparing raw healthcare
datasets before loading them into a BI warehouse.

Cleaning tasks:
- Remove duplicate records.
- Standardize inconsistent text values.
- Convert data types.
- Remove invalid records.
- Validate relationships between tables.

Author:
    Your Name

Date:
    2026-06

Process:
    - Load raw CSV files.
    - Inspect datasets.
    - Check data quality.
    - Clean and prepare datasets.
    - Validate relationships.
    - Save prepared datasets.

Input:
    data/raw/patients_data.csv
    data/raw/doctors_data.csv
    data/raw/appointments_data.csv

Output:
    data/prepared/patients_data_prepared.csv
    data/prepared/doctors_data_prepared.csv
    data/prepared/appointments_data_prepared.csv

Run command:

    uv run python -m bizintel.data_prep_hospital
"""


# ============================================================
# IMPORTS
# ============================================================

from pathlib import Path
from typing import Final

import pandas as pd

from datafun_toolkit.logger import log_path

from bizintel.utils_data import (
    check_quality,
    inspect_basic,
    load_data,
    summarize_numeric,
)

from bizintel.utils_logger import (
    LOG,
    log_header,
)


# ============================================================
# GLOBAL CONSTANTS
# ============================================================


DATA_RAW: Final[Path] = Path("data/raw")

DATA_PREPARED: Final[Path] = Path("data/prepared")


# Input files

PATIENTS_FILE: Final[Path] = (
    DATA_RAW / "patients_data.csv"
)

DOCTORS_FILE: Final[Path] = (
    DATA_RAW / "doctors_data.csv"
)

APPOINTMENTS_FILE: Final[Path] = (
    DATA_RAW / "appointments_data.csv"
)


# Output files

PATIENTS_PREPARED: Final[Path] = (
    DATA_PREPARED / "patients_data_prepared.csv"
)

DOCTORS_PREPARED: Final[Path] = (
    DATA_PREPARED / "doctors_data_prepared.csv"
)

APPOINTMENTS_PREPARED: Final[Path] = (
    DATA_PREPARED / "appointments_data_prepared.csv"
)



# ============================================================
# PREPARE PATIENTS DATA
# ============================================================


def prepare_patients(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Clean and prepare patient records.

    Cleaning rules:
    - Standardize gender values.
    - Remove missing patient IDs.
    - Convert birth dates.
    - Remove duplicates.

    Args:
        df:
            Raw patients dataframe.

    Returns:
        Prepared patients dataframe.
    """

    LOG.info("Preparing patients data")

    df = df.copy()


    # --------------------------------------------------------
    # Normalize Gender
    # --------------------------------------------------------

    LOG.info(
        "Patients Prep 1. Normalize Gender"
    )


    if "Gender" in df.columns:

        df["Gender"] = (
            df["Gender"]
            .astype(str)
            .str.strip()
            .str.lower()
        )


        gender_map = {
            "m": "Male",
            "male": "Male",
            "man": "Male",

            "f": "Female",
            "female": "Female",
            "woman": "Female",
        }


        df["Gender"] = (
            df["Gender"]
            .map(gender_map)
        )


    # --------------------------------------------------------
    # Convert BirthDate
    # --------------------------------------------------------

    LOG.info(
        "Patients Prep 2. Convert BirthDate"
    )


    if "BirthDate" in df.columns:

        df["BirthDate"] = pd.to_datetime(
            df["BirthDate"],
            errors="coerce",
        )


        invalid_dates = int(
            df["BirthDate"]
            .isna()
            .sum()
        )


        if invalid_dates > 0:

            LOG.warning(
                f"  Invalid birth dates: {invalid_dates}"
            )



    # --------------------------------------------------------
    # Remove Missing Patient IDs
    # --------------------------------------------------------

    LOG.info(
        "Patients Prep 3. Remove missing PatientID"
    )


    before = df.shape[0]


    df = df.dropna(
        subset=[
            "PatientID"
        ]
    )


    after = df.shape[0]


    LOG.info(
        f"  Removed {before-after} missing IDs"
    )



    # --------------------------------------------------------
    # Remove duplicates
    # --------------------------------------------------------

    LOG.info(
        "Patients Prep 4. Remove duplicates"
    )


    before = df.shape[0]


    df = df.drop_duplicates()


    after = df.shape[0]


    LOG.info(
        f"  Removed {before-after} duplicate rows"
    )


    LOG.info(
        f"Patients prepared: {df.shape[0]} rows"
    )


    return df



# ============================================================
# PREPARE DOCTORS DATA
# ============================================================


def prepare_doctors(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Clean and prepare doctor records.

    Cleaning rules:
    - Normalize department names.
    - Convert salary values.
    - Remove duplicates.

    Args:
        df:
            Raw doctors dataframe.

    Returns:
        Prepared doctors dataframe.
    """


    LOG.info(
        "Preparing doctors data"
    )


    df = df.copy()


    # --------------------------------------------------------
    # Normalize Department
    # --------------------------------------------------------

    LOG.info(
        "Doctors Prep 1. Normalize Department"
    )


    if "Department" in df.columns:


        df["Department"] = (
            df["Department"]
            .astype(str)
            .str.strip()
            .str.title()
        )



    # --------------------------------------------------------
    # Convert Salary
    # --------------------------------------------------------

    LOG.info(
        "Doctors Prep 2. Convert Salary"
    )


    if "Salary" in df.columns:


        df["Salary"] = pd.to_numeric(
            df["Salary"],
            errors="coerce",
        )


        bad_salary = int(
            df["Salary"]
            .isna()
            .sum()
        )


        if bad_salary > 0:

            LOG.warning(
                f"  Invalid salary values: {bad_salary}"
            )



    # --------------------------------------------------------
    # Remove duplicates
    # --------------------------------------------------------

    LOG.info(
        "Doctors Prep 3. Remove duplicates"
    )


    before = df.shape[0]


    df = df.drop_duplicates()


    after = df.shape[0]


    LOG.info(
        f"  Removed {before-after} duplicate rows"
    )


    LOG.info(
        f"Doctors prepared: {df.shape[0]} rows"
    )
    
    return df
# ============================================================
# PREPARE APPOINTMENTS DATA
# ============================================================


def prepare_appointments(
    df: pd.DataFrame,
    valid_patient_ids: set[int],
    valid_doctor_ids: set[int],
) -> pd.DataFrame:
    """
    Clean and prepare appointment records.

    Cleaning rules:
    - Convert appointment dates.
    - Convert billing amounts.
    - Remove missing values.
    - Validate PatientID relationships.
    - Validate DoctorID relationships.
    - Remove duplicates.

    Args:
        df:
            Raw appointments dataframe.

        valid_patient_ids:
            Valid PatientID values from patients table.

        valid_doctor_ids:
            Valid DoctorID values from doctors table.

    Returns:
        Prepared appointments dataframe.
    """

    LOG.info(
        "Preparing appointments data"
    )

    df = df.copy()


    # --------------------------------------------------------
    # Convert AppointmentDate
    # --------------------------------------------------------

    LOG.info(
        "Appointments Prep 1. Convert AppointmentDate"
    )


    if "AppointmentDate" in df.columns:

        df["AppointmentDate"] = pd.to_datetime(
            df["AppointmentDate"],
            errors="coerce",
        )


        invalid_dates = int(
            df["AppointmentDate"]
            .isna()
            .sum()
        )


        if invalid_dates > 0:

            LOG.warning(
                f"  Invalid appointment dates: {invalid_dates}"
            )



    # --------------------------------------------------------
    # Convert BillAmount
    # --------------------------------------------------------

    LOG.info(
        "Appointments Prep 2. Convert BillAmount"
    )


    if "BillAmount" in df.columns:


        df["BillAmount"] = pd.to_numeric(
            df["BillAmount"],
            errors="coerce",
        )


        invalid_amounts = int(
            df["BillAmount"]
            .isna()
            .sum()
        )


        if invalid_amounts > 0:

            LOG.warning(
                f"  Invalid bill amounts: {invalid_amounts}"
            )



    # --------------------------------------------------------
    # Remove missing dates and amounts
    # --------------------------------------------------------

    LOG.info(
        "Appointments Prep 3. Remove missing values"
    )


    before = df.shape[0]


    df = df.dropna(
        subset=[
            "AppointmentDate",
            "BillAmount",
        ]
    )


    after = df.shape[0]


    LOG.info(
        f"  Removed {before-after} incomplete rows"
    )



    # --------------------------------------------------------
    # Validate PatientID foreign key
    # --------------------------------------------------------

    LOG.info(
        "Appointments Prep 4. Validate PatientID"
    )


    invalid_patients = (
        ~df["PatientID"]
        .isin(valid_patient_ids)
    )


    invalid_patient_count = int(
        invalid_patients.sum()
    )


    if invalid_patient_count > 0:

        LOG.warning(
            f"  Removing {invalid_patient_count} "
            "appointments with invalid PatientID"
        )


        df = df[
            ~invalid_patients
        ]



    # --------------------------------------------------------
    # Validate DoctorID foreign key
    # --------------------------------------------------------

    LOG.info(
        "Appointments Prep 5. Validate DoctorID"
    )


    invalid_doctors = (
        ~df["DoctorID"]
        .isin(valid_doctor_ids)
    )


    invalid_doctor_count = int(
        invalid_doctors.sum()
    )


    if invalid_doctor_count > 0:

        LOG.warning(
            f"  Removing {invalid_doctor_count} "
            "appointments with invalid DoctorID"
        )


        df = df[
            ~invalid_doctors
        ]



    # --------------------------------------------------------
    # Remove duplicates
    # --------------------------------------------------------

    LOG.info(
        "Appointments Prep 6. Remove duplicates"
    )


    before = df.shape[0]


    df = df.drop_duplicates()


    after = df.shape[0]


    LOG.info(
        f"  Removed {before-after} duplicate rows"
    )


    LOG.info(
        f"Appointments prepared: {df.shape[0]} rows"
    )


    return df





# ============================================================
# SAVE PREPARED DATA
# ============================================================


def save_prepared(
    df: pd.DataFrame,
    filepath: Path,
    name: str,
) -> None:
    """
    Save prepared dataframe as CSV.

    Args:
        df:
            Prepared dataframe.

        filepath:
            Output file path.

        name:
            Dataset name for logging.
    """


    filepath.parent.mkdir(
        parents=True,
        exist_ok=True,
    )


    df.to_csv(
        filepath,
        index=False,
    )


    LOG.info(
        f"Saved {name}"
    )


    LOG.info(
        f"  Rows: {df.shape[0]}"
    )


    LOG.info(
        f"  Path: {filepath}"
    )





# ============================================================
# MAIN FUNCTION
# ============================================================


def main() -> None:
    """
    Run hospital data preparation workflow.
    """


    log_header(
        LOG,
        "BI HOSPITAL DATA PREPARATION",
    )


    LOG.info(
        "Starting hospital ETL workflow"
    )


    log_path(
        LOG,
        "Raw data:",
        DATA_RAW,
    )


    log_path(
        LOG,
        "Prepared data:",
        DATA_PREPARED,
    )



    # --------------------------------------------------------
    # LOAD DATA
    # --------------------------------------------------------

    LOG.info(
        "Task 1. LOAD DATA"
    )


    df_patients = load_data(
        PATIENTS_FILE,
        "patients",
    )


    df_doctors = load_data(
        DOCTORS_FILE,
        "doctors",
    )


    df_appointments = load_data(
        APPOINTMENTS_FILE,
        "appointments",
    )



    # --------------------------------------------------------
    # INSPECT
    # --------------------------------------------------------

    LOG.info(
        "Task 2. INSPECT DATA"
    )


    inspect_basic(
        df_patients,
        "patients",
    )


    inspect_basic(
        df_doctors,
        "doctors",
    )


    inspect_basic(
        df_appointments,
        "appointments",
    )



    # --------------------------------------------------------
    # QUALITY CHECK BEFORE
    # --------------------------------------------------------

    LOG.info(
        "Task 3. QUALITY CHECK BEFORE"
    )


    check_quality(
        df_patients,
        "patients",
    )


    check_quality(
        df_doctors,
        "doctors",
    )


    check_quality(
        df_appointments,
        "appointments",
    )



    # --------------------------------------------------------
    # PREPARE DATA
    # --------------------------------------------------------

    LOG.info(
        "Task 4. PREPARE DATA"
    )


    patients_prepared = prepare_patients(
        df_patients
    )


    doctors_prepared = prepare_doctors(
        df_doctors
    )



    valid_patient_ids = set(
        patients_prepared["PatientID"]
    )


    valid_doctor_ids = set(
        doctors_prepared["DoctorID"]
    )



    appointments_prepared = prepare_appointments(
        df_appointments,
        valid_patient_ids,
        valid_doctor_ids,
    )



    # --------------------------------------------------------
    # QUALITY CHECK AFTER
    # --------------------------------------------------------

    LOG.info(
        "Task 5. QUALITY CHECK AFTER"
    )


    check_quality(
        patients_prepared,
        "patients prepared",
    )


    check_quality(
        doctors_prepared,
        "doctors prepared",
    )


    check_quality(
        appointments_prepared,
        "appointments prepared",
    )



    # --------------------------------------------------------
    # SUMMARIZE
    # --------------------------------------------------------

    LOG.info(
        "Task 6. SUMMARIZE DATA"
    )


    summarize_numeric(
        patients_prepared,
        "patients prepared",
    )


    summarize_numeric(
        doctors_prepared,
        "doctors prepared",
    )


    summarize_numeric(
        appointments_prepared,
        "appointments prepared",
    )



    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    LOG.info(
        "Task 7. SAVE FILES"
    )


    save_prepared(
        patients_prepared,
        PATIENTS_PREPARED,
        "patients",
    )


    save_prepared(
        doctors_prepared,
        DOCTORS_PREPARED,
        "doctors",
    )


    save_prepared(
        appointments_prepared,
        APPOINTMENTS_PREPARED,
        "appointments",
    )


    LOG.info(
        "Hospital data preparation complete"
    )


# ============================================================
# EXECUTION GUARD
# ============================================================

if __name__ == "__main__":
    main()

  

"""
create_raw_data.py

Generate sample hospital datasets with realistic
data quality issues for BI data preparation.

Run:
    python create_raw_data.py
"""

from pathlib import Path
import random
import pandas as pd

random.seed(42)

# ---------------------------------------
# Create raw folder
# ---------------------------------------

RAW_FOLDER = Path("data/raw")
RAW_FOLDER.mkdir(parents=True, exist_ok=True)

# ---------------------------------------
# Sample values
# ---------------------------------------

first_names = [
    "John","Mary","James","Sarah","Michael","Emily",
    "David","Ashley","Robert","Jessica","Daniel",
    "Lisa","William","Jennifer","Joseph","Amanda",
    "Thomas","Karen","Charles","Nancy"
]

last_names = [
    "Smith","Johnson","Brown","Jones","Garcia",
    "Miller","Davis","Wilson","Taylor","Clark",
    "Hall","Young","Allen","King","Scott"
]

cities = [
    "Omaha",
    "Lincoln",
    "Kansas City",
    "Denver",
    "Chicago",
    "St Louis"
]

genders = [
    "Male",
    "male",
    "M",
    "Female",
    "female",
    "F",
    " Male ",
    " FEMALE "
]

departments = [
    "Cardiology",
    "Neurology",
    "Orthopedics",
    "Emergency",
    "Pediatrics",
    "Radiology"
]

statuses = [
    "Completed",
    "Completed",
    "Completed",
    "Cancelled",
    "Scheduled"
]

# ---------------------------------------
# Patients
# ---------------------------------------

patients = []

for pid in range(1001,1101):

    patients.append({

        "PatientID": pid,

        "FirstName": random.choice(first_names),

        "LastName": random.choice(last_names),

        "Gender": random.choice(genders),

        "BirthDate":
            f"{random.randint(1950,2010)}-"
            f"{random.randint(1,12):02d}-"
            f"{random.randint(1,28):02d}",

        "City": random.choice(cities)

    })

# add duplicate
patients.append(patients[15].copy())

# invalid birthdate
patients[8]["BirthDate"] = "invalid_date"

patients_df = pd.DataFrame(patients)

patients_df.to_csv(
    RAW_FOLDER / "patients_data.csv",
    index=False
)

# ---------------------------------------
# Doctors
# ---------------------------------------

doctors = []

for did in range(501,526):

    doctors.append({

        "DoctorID": did,

        "DoctorName":
            "Dr. " + random.choice(last_names),

        "Department": random.choice([
            "cardiology",
            "CARDIOLOGY",
            "Neurology",
            " neurology ",
            "Orthopedics",
            "Pediatrics",
            "Emergency"
        ]),

        "Salary": random.choice([
            random.randint(120000,220000),
            random.randint(120000,220000),
            random.randint(120000,220000),
            "?"
        ])

    })

# duplicate
doctors.append(doctors[3].copy())

doctors_df = pd.DataFrame(doctors)

doctors_df.to_csv(
    RAW_FOLDER / "doctors_data.csv",
    index=False
)

# ---------------------------------------
# Appointments
# ---------------------------------------

appointments = []

for aid in range(9001,9301):

    appointments.append({

        "AppointmentID": aid,

        "PatientID":
            random.randint(1001,1100),

        "DoctorID":
            random.randint(501,525),

        "AppointmentDate":
            f"2026-{random.randint(1,12):02d}-{random.randint(1,28):02d}",

        "BillAmount":
            random.choice([
                random.randint(80,750),
                random.randint(80,750),
                random.randint(80,750),
                "?"
            ]),

        "Status":
            random.choice(statuses)

    })

# invalid patient
appointments[10]["PatientID"] = 9999

# invalid doctor
appointments[20]["DoctorID"] = 999

# invalid date
appointments[30]["AppointmentDate"] = "invalid_date"

# duplicate appointment
appointments.append(appointments[50].copy())

appointments_df = pd.DataFrame(appointments)

appointments_df.to_csv(
    RAW_FOLDER / "appointments_data.csv",
    index=False
)

print("Created datasets successfully.")
print(f"Patients: {len(patients_df)}")
print(f"Doctors: {len(doctors_df)}")
print(f"Appointments: {len(appointments_df)}")

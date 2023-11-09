from .student import student
import pandas as pd

COLUMNS = [
    "cid",
    "username",
    "github",
    "course",
    "title",
    "first_name",
    "last_name",
    "gender",
    "email",
    "tutor",
    "fee_status",
    "nationality",
    "enrollment_status",
    "personal_email",
]


def cohort(n):
    students = [student() for _ in range(n)]

    data = {col: [getattr(student, col) for student in students] for col in COLUMNS}

    return pd.DataFrame(data)

from dataclasses import dataclass
from faker import Faker
import phantombunch as pb
import random
import pandas as pd


_fake = Faker()


# Distributions, biases, constants.
_tutors = [_fake.name() for _ in range(25)]
_genders_distribution = {"male": 0.65, "female": 0.34, "nonbinary": 0.01}
_course_distribution = {"acse": 0.4, "edsml": 0.4, "gems": 0.2}
_country_biases = {
    "China": 1800,
    "United Kingdom": 250,
    "India": 150,
    "United States": 100,
    "Germany": 100,
    "France": 100,
    "Hong Kong": 100,
    "Spain": 100,
    "Italy": 100,
    "Netherlands": 80,
    "Canada": 80,
}
_attributes = [
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


@dataclass
class Student:
    """A dataclass to be populated in student function."""

    cid: str
    gender: str
    nationality: str
    first_name: str
    last_name: str
    title: str
    course: str
    username: str
    email: str
    personal_email: str
    github: str
    fee_status: str
    enrollment_status: str
    tutor: str


def student():
    """Generate a random student.

    Returns
    -------
    Student

        A dataclass containing student information.

    Examples
    --------
    >>> import phantombunch as pb
    >>> pb.student()
    Student(cid=...)
    """
    gender = pb.gender(distribution=_genders_distribution)
    course = pb.course(distribution=_course_distribution)
    nationality = pb.country(bias=_country_biases)
    first_name, *_, last_name = pb.name(gender=gender, country=nationality).split()
    username = pb.username(nameval=f"{first_name} {last_name}")

    return Student(
        cid=pb.cid(),
        gender=gender,
        course=course,
        nationality=nationality,
        first_name=first_name,
        last_name=last_name,
        title=pb.title(genderval=gender),
        username=username,
        email=pb.email(domain="imperial.ac.uk"),
        personal_email=pb.email(),
        github=f"{course}-{username}",
        fee_status="home" if nationality == "United Kingdom" else "overseas",
        enrollment_status="enrolled",
        tutor=random.choice(_tutors),
    )


def cohort(n):
    """Generate a cohort of students.

    Parameters
    ----------
    n: int

        Number of students in the cohort.

    Returns
    -------
    pandas.DataFrame

        A dataframe containing student information.

    Examples
    --------
    >>> import phantombunch as pb
    >>> pb.cohort(100)  # doctest: +SKIP
    ...

    """
    students = [student() for _ in range(n)]
    data = {col: [getattr(student, col) for student in students] for col in _attributes}
    return pd.DataFrame(data)

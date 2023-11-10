from dataclasses import dataclass

import phantombunch as pb
import os

@dataclass
class Student:
    """A student."""

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
    cid = pb.cid()
    gender = pb.gender(probabilities=[0.65, 0.34, 0.01])
    nationality = pb.country(
        bias={
            "China": 3,
            "United Kingdom": 0.4,
            "Germany": 0.2,
            "India": 0.2,
            "France": 0.2,
            "Hong Kong": 0.1,
            "Spain": 0.1,
            "Italy": 0.1,
            "Netherlands": 0.1,
            "United States": 0.25,
            "Canada": 0.1,
        }
    )
    full_name = pb.name(gender=gender, country=nationality)
    first_name = full_name.split()[0]
    last_name = " ".join(full_name.split()[1:])
    title = pb.title(gender=gender)
    course = pb.course()
    username = pb.username(name=full_name)
    email = pb.email(domain="imperial.ac.uk")
    personal_email = pb.email()
    github = f"{course}-{username}"
    fee_status = "home" if nationality == "United Kingdom" else "overseas"
    enrollment_status = "enrolled"
    tutor = pb.tutor()

    return Student(
        cid=cid,
        gender=gender,
        nationality=nationality,
        first_name=first_name,
        last_name=last_name,
        title=title,
        course=course,
        username=username,
        email=email,
        personal_email=personal_email,
        github=github,
        fee_status=fee_status,
        enrollment_status=enrollment_status,
        tutor=tutor,
    )

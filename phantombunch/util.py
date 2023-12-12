import random
import re
import pandas as pd

import faker
import pycountry

GENDERS = {"male": 0.49, "female": 0.5, "nonbinary": 0.01}
COUNTRIES = {country.name: 1 for country in pycountry.countries}
TITLES = ["Mr", "Ms", "Mrs", "Miss", "Mx"]
COURSES = {"acse": 0.4, "edsml": 0.4, "gems": 0.2}

EMAIL_RE = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
# We allow 1-3 letters followed by 1-5 numbers.
USERNAME_RE = r"^[a-z]{1,3}[1-9][0-9]{1,4}$"
# We allow the second digit to be 0, 1 or 2.
CID_RE = r"^0[012][0-9]{6}$"
NAME_RE = r"^([A-Z][a-z]*)([-\s](([A-Z][a-z]*)|\([A-Z][a-z]*\)))*$"
# We allow Dr as well.
TITLE_RE = r"^(Mr|Ms|Mrs|Mx|Miss|Dr)$"
COURSE_RE = r"^(acse|edsml|gems)$"
GENDER_RE = r"^(male|female|nonbinary)$"
FEE_STATUS_RE = r"^(home|overseas|(home - elq))$"

# Country-locale mapping.
# Exposed as mapping instead of a function for performance reasons.
COUNTRY_LOCALE = {}
for country in COUNTRIES:
    for locale in faker.config.AVAILABLE_LOCALES:
        if pycountry.countries.get(name=country).alpha_2 in locale:
            COUNTRY_LOCALE[country] = locale
            break


def discrete_draw(distribution):
    """Draw a random value from a discrete distribution.

    Parameters
    ----------
    distribution: dict

        Dictionary of values and probabilities.

    Returns
    -------
    str

        Randomly selected value.

    Examples
    --------
    >>> import phantombunch as pb
    >>> pb.discrete_draw({"a": 0.5, "b": 0.5})  # doctest: +SKIP
    'a'

    """
    values = list(distribution.keys())
    probabilities = list(distribution.values())
    return random.choices(values, weights=probabilities, k=1)[0]


def valid_email(email):
    """Check if email is valid.

    Parameters
    ----------
    email: str

        Email address.

    Returns
    -------
    bool

        True if valid, otherwise False.

    Examples
    --------
    >>> import phantombunch as pb
    >>> pb.valid_email('johndoe@gmail.com')
    True
    >>> pb.valid_email('johndoe')
    False

    """
    return bool(re.match(EMAIL_RE, email))


def valid_username(username):
    """Check if username is valid.

    Parameters
    ----------
    username: str

        Username.

    Returns
    -------
    bool

        True if valid, otherwise False.

    Examples
    --------
    >>> import phantombunch as pb
    >>> pb.valid_username('johndoe')
    False
    >>> pb.valid_username('abc1234')
    True

    """
    return bool(re.match(USERNAME_RE, username))


def valid_cid(cid):
    """Check if cid is valid.

    Parameters
    ----------
    cid: str

        CID.

    Returns
    -------
    bool

        True if valid, otherwise False.

    Examples
    --------
    >>> import phantombunch as pb
    >>> pb.valid_cid('01234567')
    True
    >>> pb.valid_cid('012345678')
    False

    """
    return bool(re.match(CID_RE, cid))


def valid_name(name):
    """Check if name is valid.

    Parameters
    ----------
    name: str

        Name.

    Returns
    -------
    bool

        True if valid, otherwise False.

    Examples
    --------
    >>> import phantombunch as pb
    >>> pb.valid_name('John Doe')
    True
    >>> pb.valid_name('John')
    True
    >>> pb.valid_name('john')
    False

    """
    return bool(re.match(NAME_RE, name))


def valid_title(title):
    """Check if title is valid.

    Parameters
    ----------
    title: str

        Title.

    Returns
    -------
    bool

        True if valid, otherwise False.

    Examples
    --------
    >>> import phantombunch as pb
    >>> pb.valid_title('Mr')
    True
    >>> pb.valid_title('mr')
    False

    """
    return bool(re.match(TITLE_RE, title))


def valid_course(course):
    """Check if course is valid.

    Parameters
    ----------
    course: str

        Course.

    Returns
    -------
    bool

        True if valid, otherwise False.

    Examples
    --------
    >>> import phantombunch as pb
    >>> pb.valid_course('acse')
    True
    >>> pb.valid_course('acse1')
    False

    """
    return bool(re.match(COURSE_RE, course))


def valid_gender(gender):
    """Check if gender is valid.

    Parameters
    ----------
    gender: str

        Gender.

    Returns
    -------
    bool

        True if valid, otherwise False.

    Examples
    --------
    >>> import phantombunch as pb
    >>> pb.valid_gender('female')
    True
    >>> pb.valid_gender('Female')
    False

    """
    return bool(re.match(GENDER_RE, gender))


def valid_fee_status(fee_status):
    """Check if fee_status is valid.

    Parameters
    ----------
    fee_status: str

        Fee status.

    Returns
    -------
    bool

        True if valid, otherwise False.

    Examples
    --------
    >>> import phantombunch as pb
    >>> pb.valid_fee_status('home')
    True
    >>> pb.valid_fee_status('overseas')
    True
    >>> pb.valid_fee_status('home1')
    False

    """
    return bool(re.match(FEE_STATUS_RE, fee_status))


def valid_country(country):
    """Check if country is valid.

    Parameters
    ----------
    country: str

        Country.

    Returns
    -------
    bool

        True if valid, otherwise False.

    Examples
    --------
    >>> import phantombunch as pb
    >>> pb.valid_country('United Kingdom')
    True
    >>> pb.valid_country('United Kingdom1')
    False

    """
    allowed_countries = list(COUNTRIES.keys()) + ["Taiwan", "Syria", "Columbia", "Turkey"]
    return country in allowed_countries


def valid_mark(mark):
    """Check if mark is valid.

    Parameters
    ----------
    mark: float

        Mark.

    Returns
    -------
    bool

        True if valid, otherwise False.

    """
    return 0 <= mark <= 100

def valid_cohort(cohort):
    """Check if cohort is valid.

    Parameters
    ----------
    cohort: DataFrame

            Cohort.

    Returns
    -------
    bool

        True if valid, otherwise False.

    """
    for col in cohort.columns:
        if col != "username" and ("name" in col or col == "tutor"):
            data = "name"
        elif "email" in col:
            data = "email"
        elif col in ["github", "enrollment_status"]:
            continue
        elif col == "nationality":
            data = "country"
        else:
            data = col
        validation_function = globals()[f"valid_{data}"]
        if not cohort[col].map(validation_function).all():
            print(col, validation_function, "fail")
            return False
    else:
        return True
    

def valid_assignment(assignment, cohort=None, exclude_usernames=None):
    """Check if assignment is valid.

    Parameters
    ----------
    assignment: DataFrame
    
        Assignment.

    Returns
    -------
    bool

        True if valid, otherwise False.

    """
    if not isinstance(cohort, pd.DataFrame):
        # Enforce CID to be read as a string.
        cohort = pd.read_csv(cohort, dtype={'cid': str})
    
    if not valid_cohort(cohort):
        raise ValueError("Invalid cohort.")

    if not set(assignment.columns) <= {"username", "mark", "feedback"}:
        print(f'Wrong column names {assignment.columns=}')
        return False
    elif not assignment["username"].map(valid_username).all():
        for username in assignment["username"]:
            if not valid_username(username):
                print(username, "not valid")
        return False
    elif not assignment["mark"].map(valid_mark).all():
        for mark in assignment["mark"]:
            if not valid_mark(mark):
                print(mark, "not valid")
        return False
    elif cohort is not None:
        exclude_usernames = exclude_usernames or []
        # Check that the usernames are as expected.
        if not (set(assignment["username"]) - set(exclude_usernames)) <= set(cohort["username"]):
            for username in set(assignment["username"]) - set(exclude_usernames):
                if username not in set(cohort["username"]):
                    print(username, "not in cohort")
            return False
    elif len(set(assignment["username"])) != len(assignment):
        # There are duplicated in the usernames.
        return False

    return True
        
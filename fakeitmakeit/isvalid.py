import re

import pandas as pd
import fakeitmakeit.util as pbu

EMAIL_RE = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
# We allow 1-3 lowercase letters followed by 1-5 numbers. First number is never zero.
USERNAME_RE = r"^[a-z]{1,3}[1-9][0-9]{1,4}$"
# We allow the second digit to be 0, 1 or 2.
CID_RE = r"^0[012][0-9]{6}$"
NAME_RE = r"^([A-Z][a-z]*)([-\s](([A-Z][a-z]*)|\([A-Z][a-z]*\)))*$"
# We allow Dr as well.
TITLE_RE = r"^(Mr|Ms|Mrs|Mx|Miss|Dr)$"
COURSE_RE = r"^(acse|edsml|gems)$"
GENDER_RE = r"^(male|female|nonbinary)$"
FEE_STATUS_RE = r"^(home|overseas|(home - elq))$"


def email(value):
    """Check if ``value`` is a valid email.

    Parameters
    ----------
    value: str

        Email.

    Returns
    -------
    bool

        ``True`` if valid, otherwise ``False``.

    Examples
    --------
    >>> import phantombunch as pb
    >>> pb.isvalid.email('nikola.tesla@gmail.com')
    True
    >>> pb.isvalid.email('nikola.tesla(at)gmail')
    False

    """
    return bool(re.match(EMAIL_RE, value))


def username(value):
    """Check if ``value`` is a valid username.

    Parameters
    ----------
    value: str

        Username.

    Returns
    -------
    bool

        ``True`` if valid, otherwise ``False``.

    Examples
    --------
    >>> import phantombunch as pb
    >>> pb.isvalid.username('johndoe')
    False
    >>> pb.isvalid.username('abc1234')
    True

    """
    return bool(re.match(USERNAME_RE, value))


def cid(value):
    """Check if ``value`` is a valid CID.

    Parameters
    ----------
    value: str

        CID.

    Returns
    -------
    bool

        ``True`` if valid, otherwise ``False``.

    Examples
    --------
    >>> import phantombunch as pb
    >>> pb.isvalid.cid('01234567')
    True
    >>> pb.isvalid.cid('012345678')  # 9 digits
    False

    """
    return bool(re.match(CID_RE, value))


def name(value):
    """Check if ``value`` is a valid name.

    Parameters
    ----------
    value: str

        Name.

    Returns
    -------
    bool

        ``True`` if valid, otherwise ``False``.

    Examples
    --------
    >>> import phantombunch as pb
    >>> pb.isvalid.name('Albert Einstein')
    True
    >>> pb.isvalid.name('Albert')
    True
    >>> pb.isvalid.name('john')
    False
    >>> pb.isvalid.name('Nikola_Tesla')
    False

    """
    return bool(re.match(NAME_RE, value))


def title(value):
    """Check if ``value`` is a valid title.

    Parameters
    ----------
    value: str

        Title.

    Returns
    -------
    bool

        ``True`` if valid, otherwise ``False``.

    Examples
    --------
    >>> import phantombunch as pb
    >>> pb.isvalid.title('Mr')
    True
    >>> pb.isvalid.title('mr')
    False
    >>> pb.isvalid.title('Herr')
    False

    """
    return bool(re.match(TITLE_RE, value))


def course(value):
    """Check if ``value`` is a valid course.

    Parameters
    ----------
    value: str

        Course.

    Returns
    -------
    bool

        ``True`` if valid, otherwise ``False``.

    Examples
    --------
    >>> import phantombunch as pb
    >>> pb.isvalid.course('acse')
    True
    >>> pb.isvalid.course('a_very_cool_course')
    False

    """
    return bool(re.match(COURSE_RE, value))


def gender(value):
    """Check if ``value`` is a valid gender.

    Parameters
    ----------
    value: str

        Gender.

    Returns
    -------
    bool

        ``True`` if valid, otherwise ``False``.

    Examples
    --------
    >>> import phantombunch as pb
    >>> pb.isvalid.gender('female')
    True
    >>> pb.isvalid.gender('Female')
    False

    """
    return bool(re.match(GENDER_RE, value))


def fee_status(value):
    """Check if ``value`` is a valid fee status.

    Parameters
    ----------
    value: str

        Fee status.

    Returns
    -------
    bool

        ``True`` if valid, otherwise ``False``.

    Examples
    --------
    >>> import phantombunch as pb
    >>> pb.isvalid.fee_status('home')
    True
    >>> pb.isvalid.fee_status('overseas')
    True
    >>> pb.isvalid.fee_status('home1')
    False

    """
    return bool(re.match(FEE_STATUS_RE, value))


def country(value):
    """Check if ``value`` is a valid country.

    Parameters
    ----------
    value: str

        Country.

    Returns
    -------
    bool

        ``True`` if valid, otherwise ``False``.

    Examples
    --------
    >>> import phantombunch as pb
    >>> pb.isvalid.country('United Kingdom')
    True
    >>> pb.isvalid.country('Neverland')
    False

    """
    allowed_countries = set(pbu.COUNTRIES.keys()) | {
        "Taiwan",
        "Syria",
        "Columbia",
        "Turkey",
    }
    return value in allowed_countries


def mark(value):
    """Check if ``value`` is a valid mark.

    Parameters
    ----------
    value: numbers.Real

        Mark.

    Returns
    -------
    bool

        ``True`` if valid, otherwise ``False``.

    Examples
    --------
    >>> import phantombunch as pb
    >>> pb.isvalid.mark(100)
    True
    >>> pb.isvalid.mark(101)
    False
    >>> pb.isvalid.mark(-1)
    False

    """
    return 0 <= value <= 100


def cohort(value):
    """Check if ``value`` is a valid cohort.

    Parameters
    ----------
    value: pd.DataFrame

        Cohort.

    Returns
    -------
    bool

        ``True`` if valid, otherwise ``False``.

    """
    for col in value.columns:
        if col != "username" and ("name" in col or col == "tutor"):
            data_type = "name"
        elif "email" in col:
            data_type = "email"
        elif col in ["github", "enrollment_status"]:
            continue
        elif col == "nationality":
            data_type = "country"
        else:
            data_type = col
        validation_function = globals()[f"{data_type}"]
        if not value[col].map(validation_function).all():
            print(
                col, validation_function, "fail"
            )  # replace with logging in the future
            return False
    else:
        return True


def assignment(value, valid_cohort=None, exclude_usernames=None):
    """Check if ``value`` is a valid assignment.

    Parameters
    ----------
    value: pd.DataFrame

        Assignment.

    Returns
    -------
    bool

        ``True`` if valid, otherwise ``False``.

    """
    if not isinstance(valid_cohort, pd.DataFrame):
        # Enforce CID to be read as a string.
        valid_cohort = pd.read_csv(valid_cohort, dtype={"cid": str})

    if not cohort(valid_cohort):
        raise ValueError("Invalid valid_cohort passed.")

    if not set(value.columns) <= {"username", "mark", "feedback"}:
        print(f"Wrong column names {value.columns=}")
        return False
    # elif not value.username.map(username).all():
    #     # Find the invalid usernames for easier debugging.
    #     for u in value.username:
    #         if not username(u):
    #             print(u, "not valid")
    #     return False
    elif not value["mark"].map(mark).all():
        for m in value["mark"]:
            if not mark(m):
                print(m, "not valid")
        return False
    elif cohort is not None:
        exclude_usernames = exclude_usernames or []
        # Check that the usernames are as expected.
        if not (set(value.username) - set(exclude_usernames)) <= set(
            valid_cohort["username"]
        ):
            for u in set(value.username) - set(exclude_usernames):
                if u not in cohort["username"].values:
                    print(u, "not in cohort")
            return False
    elif value.username.duplicated().any():
        # There are duplicates in the usernames.
        return False

    return True

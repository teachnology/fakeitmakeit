import re

import pandas as pd

import numbers

import fakeitmakeit.util as fmu


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
    >>> import fakeitmakeit as fm
    >>> fm.isvalid.email('nikola.tesla@gmail.com')
    True
    >>> fm.isvalid.email('nikola.tesla(at)gmail')
    False

    """
    EMAIL_RE = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
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
    >>> import fakeitmakeit as fm
    >>> fm.isvalid.username('johndoe')
    False
    >>> fm.isvalid.username('abc1234')
    True

    """
    # We allow 1-3 lowercase letters followed by 1-5 numbers - first number is never 0.
    USERNAME_RE = r"^[a-z]{1,3}[1-9][0-9]{1,4}$"
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
    >>> import fakeitmakeit as fm
    >>> fm.isvalid.cid('01234567')
    True
    >>> fm.isvalid.cid('012345678')  # 9 digits
    False

    """
    # We allow the second digit to be 0, 1, or 2.
    CID_RE = r"^0[012][0-9]{6}$"
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
    >>> import fakeitmakeit as fm
    >>> fm.isvalid.name('Albert Einstein')
    True
    >>> fm.isvalid.name('Albert')
    True
    >>> fm.isvalid.name('john')
    False
    >>> fm.isvalid.name('Nikola_Tesla')
    False

    """
    NAME_RE = r"^([A-Z][a-z]*)([-\s](([A-Z][a-z]*)|\([A-Z][a-z]*\)))*$"
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
    >>> import fakeitmakeit as fm
    >>> fm.isvalid.title('Mr')
    True
    >>> fm.isvalid.title('mr')
    False
    >>> fm.isvalid.title('Herr')
    False

    """
    TITLE_RE = r"^(Mr|Ms|Mrs|Mx|Miss|Dr)$"
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
    >>> import fakeitmakeit as fm
    >>> fm.isvalid.course('acse')
    True
    >>> fm.isvalid.course('a_very_cool_course')
    False

    """
    COURSE_RE = r"^(acse|edsml|gems)$"
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
    >>> import fakeitmakeit as fm
    >>> fm.isvalid.gender('female')
    True
    >>> fm.isvalid.gender('Female')
    False

    """
    GENDER_RE = r"^(male|female|nonbinary)$"
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
    >>> import fakeitmakeit as fm
    >>> fm.isvalid.fee_status('home')
    True
    >>> fm.isvalid.fee_status('overseas')
    True
    >>> fm.isvalid.fee_status('home1')
    False

    """
    FEE_STATUS_RE = r"^(home|overseas|(home - elq))$"
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
    >>> import fakeitmakeit as fm
    >>> fm.isvalid.country('United Kingdom')
    True
    >>> fm.isvalid.country('Neverland')
    False

    """
    allowed_countries = set(fmu.COUNTRIES.keys()) | {
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
    >>> import fakeitmakeit as fm
    >>> fm.isvalid.mark(100)
    True
    >>> fm.isvalid.mark(101)
    False
    >>> fm.isvalid.mark(-1)
    False

    """
    return isinstance(value, numbers.Real) and (0 <= value <= 100)


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

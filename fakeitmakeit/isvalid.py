import logging
import numbers
import re

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


def assignment(value, valid_usernames=None):
    """Check if ``value`` is a valid assignment.

    Parameters
    ----------
    value: pd.DataFrame

        Assignment.

    valid_usernames: Iterable[str], optional

        Iterable of valid usernames.

    Returns
    -------
    bool

        ``True`` if valid, otherwise ``False``.

    Examples
    --------
    >>> import fakeitmakeit as fm
    >>> import pandas as pd
    >>> value = pd.DataFrame({
    ...     "username": ["abc123", "sw4321"],
    ...     "mark": [50.1, 70],
    ...     "feedback": ["feedback 1", "feedback 2"]
    ... })
    >>> value = value.set_index("username")
    >>> fm.isvalid.assignment(value)
    True

    """
    if valid_usernames is not None and not all(map(username, valid_usernames)):
        invalid = [u for u in valid_usernames if not username(u)]
        logging.error(f"Invalid usernames in valid_usernames: {invalid}")
        raise ValueError("Invalid username(s) in valid_username.")

    # Check that indicies are valid usernames.
    if not value.index.map(username).all():
        invalid = value.index[~value.index.map(username)]
        logging.warning(f"Invalid usernames: {invalid.tolist()}")
        return False

    # Check the index name.
    if value.index.name != "username":
        logging.warning(
            f"Invalid index name {value.index.name} - it must be 'username'."
        )
        return False

    # Check if there are any repeated usernames.
    if not value.index.is_unique:
        invalid = value.index[value.index.duplicated()]
        logging.warning(f"There are duplicate usernames: {invalid.tolist()}.")
        return False

    # Check if the columns are as expected.
    if not set(value.columns) <= {"mark", "feedback"}:
        logging.warning(
            f"Invalid column names {set(value.columns) - {'mark', 'feedback'}}."
        )
        return False

    # Check the marks column.
    if not value["mark"].map(mark).all():
        logging.warning(
            f"Invalid marks: {value['mark'][~value['mark'].map(mark)].tolist()}."
        )
        return False

    # Check the feedback column.
    if not (value["feedback"].map(type) == str).all():
        invalid = value["feedback"][~value["feedback"].map(type) == str]
        logging.warning(f"Invalid feedback: {invalid.tolist()}.")
        return False

    if valid_usernames is not None:
        if not (set(value.index) <= set(valid_usernames)):
            invalid = set(value.index) - set(valid_usernames)
            logging.warning(f"Invalid usernames in value.index: {invalid}.")
            return False

    return True


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
    # Check that indicies are valid usernames.
    if not value.index.map(username).all():
        invalid = value.index[~value.index.map(username)]
        logging.warning(f"Invalid usernames: {invalid.tolist()}")
        return False

    # Check the index name.
    if value.index.name != "username":
        logging.warning(
            f"Invalid index name {value.index.name} - it must be 'username'."
        )
        return False

    # Check if there are any repeated usernames.
    if not value.index.is_unique:
        invalid = value.index[value.index.duplicated()]
        logging.warning(f"There are duplicate usernames: {invalid.tolist()}.")
        return False

    # Check other columns.
    for col in set(value.columns) - {"username", "github", "enrollment_status"}:
        if "name" in col or col == "tutor":
            data_type = "name"
        elif "email" in col:
            data_type = "email"
        elif col == "nationality":
            data_type = "country"
        else:
            data_type = col

        validation_function = globals()[f"{data_type}"]
        if not value[col].map(validation_function).all():
            invalid = value[col][~value[col].map(validation_function)]
            logging.warning(f'Errors in column "{col}": {invalid.tolist()}.')
            return False
    else:
        return True

import random
import re

import faker
import pycountry

GENDERS = {"male": 0.49, "female": 0.5, "nonbinary": 0.01}
COUNTRIES = {country.name: 1 for country in pycountry.countries}
TITLES = ["Mr", "Ms", "Mrs", "Miss", "Mx"]
COURSES = {"acse": 0.4, "edsml": 0.4, "gems": 0.2}

EMAIL_RE = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

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

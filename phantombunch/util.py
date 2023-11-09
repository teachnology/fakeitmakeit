import pycountry
import faker
import re
import collections

COUNTRIES = [country.name for country in pycountry.countries]
GENDERS = {"male": 0.49, "female": 0.5, "nonbinary": 0.01}
COURSES = {"acse": 0.4, "edsml": 0.4, "gems": 0.2}
TITLES = ["Mr", "Ms", "Mrs"]
TUTORS = [faker.Faker().name() for _ in range(25)]


def locale(country):
    """Return a locale for the given country.

    Parameters
    ----------
    country: str

        Country name.

    Returns
    -------
    str

        Locale if found, otherwise None.

    """
    alpha_2 = pycountry.countries.get(name=country).alpha_2
    for locale in faker.config.AVAILABLE_LOCALES:
        if alpha_2 in locale:
            return locale
    else:
        return None


def valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))
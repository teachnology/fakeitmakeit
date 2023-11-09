from faker import Faker
import random
import pycountry
import phantombunch.util as util
import numpy as np
import re
import string

fake = Faker()


def cid():
    """Generate a random 8-digit CID number.

    The first digit is always 0, whereas the second digit is randomly 1 or 2. The remaining 6 digits are randomly generated between 0 and 9.

    Returns
    -------
    str

            Randomly generated CID number.

    """
    # The first digit is always 0.
    number = "0"
    # The second digit is randomly 1 or 2.
    number += str(random.choice([1, 2]))
    # Generate the remaining 6 digits randomly between 0 and 9.
    number += "".join(str(random.randint(0, 9)) for _ in range(6))

    return number


def gender(values=list(util.GENDERS.keys()), probabilities=list(util.GENDERS.values())):
    """Generate a random gender.

    Possible genders are passed via ``values`` and probabilities via ````
    probabilities. The values in ``probabilities`` does not have to sum to 1
    because selections will be made according to the relative weights.

    Parameters
    ----------
    values: collections.abc.Sequence

        Genders to choose from.

    probabilities: collections.abc.Sequence

        Probabilities of selecting gender.

    Returns
    -------
    str

        Randomly generated gender.

    """
    return random.choices(values, weights=probabilities, k=1)[0]


def country(values=list(util.COUNTRIES), bias=None):
    """Generate a random country.

    Possible countries are passed via ``values``. If the probability of some
    countries should be increased, then a dictionary of country names and their
    relative probabilities. If ``bias`` is not provided, then all countries are
    equally likely. The values in ``bias`` does not have to sum to 1 because
    selections will be made according to the relative weights.

    Parameters
    ----------
    values: collections.abc.Sequence

        Countries to choose from.

    bias: dict

        Dictionary of countries and their relative probabilities.

    Returns
    -------
    str

        Randomly generated country.

    """
    if bias is not None:
        if not all(country in values for country in bias.keys()):
            raise ValueError("The countries in `bias` must be present in `values`.")

        # Normalize the probabilities so that they sum to 1 and multipy with 100
        # to get the frequencies at which they should be added to values to
        # increase bias.
        frequency = (
            np.array(list(bias.values()))
            / np.linalg.norm(list(bias.values()))
            * len(values)
            / 100
        )

        for country, frequency in zip(bias.keys(), frequency):
            # Add the country more times to increase its probability.
            values.extend([country] * int(frequency))

    return random.choice(values)


def name(gender=None, country=None, romanized=True):
    """Generate a random name.

    If ``romanized`` is True, then the romanized version of the name is returned
    if possible. Otherwise, the name with the default locale is returned.

    Parameters
    ----------
    gender: str

        Gender of the person.

    country: str

        Country of the person.

    romanized: bool

        Whether to return the romanized version of the name.

    Returns
    -------
    str

        Randomly generated name.

    """
    locale = util.locale(country) if country is not None else None
    fake = Faker(locale) if locale is not None else Faker()

    if romanized and hasattr(fake, "romanized_name"):
        return fake.romanized_name()

    method = f"name_{gender}" if gender is not None else "name"

    # Not all countries have names for different genders.
    try:
        res = getattr(fake, method)()
    except AttributeError:
        res = fake.name()

    if not res.isascii():
        res = getattr(Faker(), method)()

    # Remove suffixes and prefixes - PhD, words with dots and all caps.
    pattern = r"\b(?:[A-Z]+\b|PhD|Dr\(a\)|,|\w*\.\w*)"
    return re.sub(pattern, "", res).strip()


def title(gender=None):
    """Generate a random title.

    Parameters
    ----------
    gender: str

        Person's gender.

    Returns
    -------
    str

        Randomly generated title.

    """
    if gender == "male":
        return "Mr"
    elif gender == "female":
        return random.choice(["Ms", "Mrs"])
    else:
        return random.choice(util.TITLES)


def course(values=list(util.COURSES.keys()), probabilities=list(util.COURSES.values())):
    """Generate a random course.

    Possible courses are passed via ``values`` and probabilities via ````
    probabilities. The values in ``probabilities`` does not have to sum to 1
    because selections will be made according to the relative weights.

    Parameters
    ----------
    values: collections.abc.Sequence

        Courses to choose from.

    probabilities: collections.abc.Sequence

        Probabilities of selecting courses.

    Returns
    -------
    str

        Randomly generated course.

    """
    return random.choices(values, weights=probabilities, k=1)[0]


def username(name):
    """Generate a random username.

    The username is generated from the first letter of the first name, the first
    letter of the last name and a random number between 2 and 4 digits. The
    first digit of the number is never zero. The letters are lowercase.

    Parameters
    ----------
    name: str

        Person's name.

    Returns
    -------
    str

        Randomly generated username.

    """
    # Get the first letter of the first name.
    first_letter, *_ = name.casefold().split()[0]

    # Get the first letter of the last name.
    last_letter, *_ = name.casefold().split()[-1]

    # Generate a random middle lowercase letter (can be any lowercase letter).
    middle_letter = random.choice(string.ascii_lowercase)

    # Randomly decide if the string will have 2 or 3 letters.
    if random.choice([2, 3]) == 3:
        letters = first_letter + middle_letter + last_letter
    else:
        letters = first_letter + last_letter

    # Generate a random number between 2 and 4 digits where the first digit is not zero.
    num_digits = random.choice([2, 3, 4])
    numbers = str(random.randint(1, 9))  # First digit is never zero
    for _ in range(num_digits - 1):
        numbers += str(random.randint(0, 9))

    # Combine letters and numbers to form the string
    return letters + numbers


def email(domain=None):
    """Generate a random email.

    If ``domain`` is not provided, then a random email is generated. Otherwise,
    the email is generated with the provided domain.

    Parameters
    ----------
    domain: str

        Domain of the email.

    Returns
    -------
    str

        Randomly generated email.

    """
    fake = Faker()
    if domain is None:
        return fake.email()
    else:
        prefix = fake.email().split("@")[0]
        return prefix + "@" + domain

import random
import re
import string

from faker import Faker

import phantombunch.util as pbu


def cid() -> str:
    """Generate a random 8-digit CID number.

    The first digit is always 0, whereas the second digit is 1 or 2. The
    remaining 6 digits are randomly generated between 0 and 9.

    Returns
    -------
    str

        Randomly generated CID number.

    Examples
    --------
    >>> import phantombunch as pb
    >>> pb.cid()  # doctest: +SKIP
    "01234567"

    """
    # The first digit is always 0.
    number = "0"

    # The second digit is randomly 1 or 2.
    number += str(random.choice([1, 2]))

    # Generate the remaining 6 digits randomly between 0 and 9.
    number += "".join(str(random.randint(0, 9)) for _ in range(6))

    return number


def gender(distribution=dict(pbu.GENDERS)) -> str:
    """Generate a random gender.

    Possible genders and their relative probabilities are passed via
    ``distribution``. It is a dictionary where keys are possible output values
    and dictionary values are relative probablilities. The values in
    ``distribution`` do not have to sum to 1 because selections will be made
    according to the relative weights.

    Parameters
    ----------
    distribution: dict

        Keys are possible output values and dictionary values are relative
        probablilities. For instance, ``{"male": 0.5, "female": 0.5}``.

    Returns
    -------
    str

        Randomly generated gender.

    Examples
    --------
    >>> import phantombunch as pb
    >>> pb.gender()  # doctest: +SKIP
    'male'

    """
    return pbu.discrete_draw(distribution)


def title(genderval=None, use_period=False):
    """Generate a random title.

    If gender, via ``genderval``, is provided, then the title is generated
    according to it. Otherwise, the gender and accordingly the title is
    generated randomly.

    For further details, refer to:
    - https://www.grammarly.com/blog/ms-mrs-miss-difference/
    - https://publishing.rcseng.ac.uk/doi/pdf/10.1308/rcsbull.2021.141

    Parameters
    ----------
    genderval: str

        Person's gender.

    use_period: bool

        Whether to use a period at the end of the title.

    Returns
    -------
    str

        Randomly generated title according to the gender.

    Examples
    --------
    >>> import phantombunch as pb
    >>> pb.title('male')
    'Mr'
    >>> pb.title()  # doctest: +SKIP
    'Mx'
    >>> pb.title(use_period=True)  # doctest: +SKIP
    'Mrs.'

    """
    genderval = genderval or gender()
    if genderval == "male":
        res = "Mr"
    elif genderval == "female":
        res = random.choice(["Ms", "Mrs", "Miss"])
    elif genderval == "nonbinary":
        res = "Mx"
    else:
        raise ValueError(f"Invalid gender: {genderval=}")

    return f"{res}." if use_period else res


def course(values=list(pbu.COURSES.keys()), probabilities=list(pbu.COURSES.values())):
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


def country(values=list(pbu.COUNTRIES), bias=None):
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
    base_probability = 1 / len(values)
    p_dict = {country: base_probability for country in values}
    p_dict |= bias or {}

    return random.choices(list(p_dict.keys()), weights=list(p_dict.values()), k=1)[0]


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
    locale = pbu.locale(country) if country is not None else None
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


def tutor():
    """Generate a random tutor.

    Returns
    -------
    str

        Randomly generated tutor.

    """
    return random.choice(pbu.TUTORS)

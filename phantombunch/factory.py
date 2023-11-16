import random
import re
import string

import numpy as np
from faker import Faker

import phantombunch.util as pbu


def cid() -> str:
    """Generate a random 8-digit CID number.

    The first digit is always 0, whereas the second digit is 1, or 2. The
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


def title(genderval=None, use_period=False) -> str:
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


def course(distribution=dict(pbu.COURSES)) -> str:
    """Generate a random course.

    Possible courses and their relative probabilities are passed via
    ``distribution``. It is a dictionary where keys are possible output values
    and dictionary values are relative probablilities. The values in
    ``distribution`` do not have to sum to 1 because selections will be made
    according to the relative weights.

    Parameters
    ----------
    distribution: dict

        Keys are possible output values and dictionary values are relative
        probablilities. For instance, ``{"course1": 0.5, "course2": 0.5}``.

    Returns
    -------
    str

        Randomly generated course.

    Examples
    --------
    >>> import phantombunch as pb
    >>> pb.course()  # doctest: +SKIP
    'acse'

    """
    return pbu.discrete_draw(distribution)


def country(distribution=dict(pbu.COUNTRIES), bias=None):
    """Generate a random country.

    Distribution is passed via ``distribution``. It is a dictionary where keys
    are possible output values and dictionary values are relative
    probablilities. The values in ``distribution`` do not have to sum to 1
    because selections will be made according to the relative weights. By
    default, all countries are equally likely and their relative probablility is
    1. To modify the default probablilities, pass a dictionary of countries and
    their relative probabilities via ``bias``. Internally, ``distribution |=
    bias`` is calculated.

    Parameters
    ----------
    distribution: dict

        Keys are possible output values and dictionary values are relative
        probablilities.

    Returns
    -------
    str

        Randomly generated country.

    Examples
    --------
    >>> import phantombunch as pb
    >>> pb.country()  # doctest: +SKIP
    'United Kingdom'
    >>> pb.country(bias={'China': 0.5, 'United Kingdom': 0.2})  # doctest: +SKIP
    'China'
    >>> pb.country(distribution={}, bias={'France': 1})
    'France'

    """
    distribution |= bias or {}
    return pbu.discrete_draw(distribution)


def username(nameval=None):
    """Generate a random username.

    The username is the combination of 2-3 lowercase letters and a random number
    with 2 to 4 digits. The first letter of the username is the first letter of
    the first name, whereas the the last letter of the username is the first
    letter of the last name. Letters are followed with a random integer between
    2 and 4 digits. The first digit of the number is never zero.

    Parameters
    ----------
    nameval: str

        Person's name.

    Returns
    -------
    str

        Randomly generated username.

    Examples
    --------
    >>> import phantombunch as pb
    >>> pb.username('John Smith')  # doctest: +SKIP
    'jws4122'

    """
    nameval = nameval or name()

    # Get the first letter of the first name.
    first_letter, *_ = nameval.casefold().split()[0]

    # Get the first letter of the last name.
    last_letter, *_ = nameval.casefold().split()[-1]

    # Randomly decide if the string will have 2 or 3 letters.
    if random.choice([2, 3]) == 3:
        # Generate a random middle lowercase letter (can be any lowercase letter).
        middle_letter = random.choice(string.ascii_lowercase)
        letters = first_letter + middle_letter + last_letter
    else:
        letters = first_letter + last_letter

    # Generate a random number between 2 and 4 digits where the first digit is not zero.
    num_digits = random.choice([2, 3, 4])
    numbers = str(random.randint(1, 9))  # First digit is never zero
    for _ in range(num_digits - 1):
        numbers += str(random.randint(0, 9))

    return letters + numbers


def email(domain=None):
    """Generate a random email.

    If ``domain`` is not provided, then an email with a random domain is
    generated. Otherwise, the email is generated with the provided domain.

    Parameters
    ----------
    domain: str

        Domain of the email.

    Returns
    -------
    str

        Randomly generated email.

    Examples
    --------
    >>> import phantombunch as pb
    >>> pb.email()  # doctest: +SKIP
    'somerandomemail@domain.com'
    >>> pb.email(domain='myuniversity.ac.uk')  # doctest: +SKIP
    'john.doe@myuniversity.ac.uk'

    """
    fake = Faker()
    domain = domain or fake.domain_name()
    return f"{fake.user_name()}@{domain}"


def name(gender=None, country=None, romanized=True):
    """Generate a random name.

    This function uses Faker to generate a random name. Depending on the
    ``country`` and ``gender`` parameters, the name is generated according to
    the locale and by calling the appropriate method from Faker. If
    ``romanized`` is True, then the romanized version of the name is returned if
    possible, e.g. Chinese names are returned in English alphabet. Otherwise,
    the name with the default Faker locale is returned.

    Parameters
    ----------
    gender: str

        Gender of the person.

    country: str

        Country of the person.

    romanized: bool

        Whether to return the romanized version of the name. Whether to return
        only ASCII characters. If impossible for particular gender and country,
        then the default Faker locale is used.

    Returns
    -------
    str

        Randomly generated name.

    Examples
    --------
    >>> import phantombunch as pb
    >>> pb.name()  # doctest: +SKIP
    'John Smith'
    >>> pb.name(country='China')  # doctest: +SKIP
    '张三'
    >>> pb.name(country='China', romanized=True)  # doctest: +SKIP
    'Zhang San'
    >>> pb.name(gender='female', country='Germany')  # doctest: +SKIP
    'Anna Schmidt'

    """
    locale = pbu.COUNTRY_LOCALE.get(country, None)
    fake = Faker(locale)

    # Romanized is available only for some countries.
    if romanized and hasattr(fake, "romanized_name"):
        return fake.romanized_name()

    # Depending on the gender, we call the appropriate method from Faker.
    method = f"name_{gender}" if gender is not None else "name"

    # Not all countries have names for different genders.
    try:
        res = getattr(fake, method)()
    except AttributeError:
        res = fake.name()

    if romanized and not res.isascii():
        res = getattr(Faker(), method)()

    # Remove suffixes and prefixes - Mr, PhD, words with dots and all caps.
    # This is not exhaustive and some names might still contain some of these.
    pattern = r"\b(?:[A-Z]+\b|PhD|Dr\(a\)|,|Dr|Mr|Mrs|Ms|Miss|\w*\.\w*)"

    return re.sub(pattern, "", res).strip()


def mark(mean=65, sd=6, fail_probability=0.02):
    """Generate a random mark.

    A mark between 0 and 100 is generated from a normal distribution with the
    given mean and standard deviation. There is a probability
    ``fail_probability`` that the mark will be 0.

    Parameters
    ----------
    mean: float

        Mean of the normal distribution.

    sd: float

            Standard deviation of the normal distribution.

    fail_probability: float

        Probability that the mark will be 0.

    Returns
    -------
    float

        Randomly generated mark.

    Examples
    --------
    >>> import phantombunch as pb
    >>> pb.mark(65, 10)  # doctest: +SKIP
    71

    """
    # Generate a random float between 0 and 1.
    if np.random.rand() < fail_probability:
        # Return 0 with a probability of fail_probability
        return 0.0
    else:
        # Generate a random number from a normal distribution with the given
        # mean and standard deviation.
        number = np.random.normal(mean, sd)
        # Clip the number to be be between 0 and 100.
        number = np.clip(number, 0, 100)
        # Round the number to two decimal places
        return round(number, 2)


def feedback(nmin=1, nmax=3):
    """Generate a random feedback.

    The feedback is generated by Faker and consists of nmin to nmax paragraphs.

    Parameters
    ----------
    nmin: int

        Minimum number of paragraphs.

    nmax: int

        Maximum number of paragraphs.

    Returns
    -------
    str

        Randomly generated feedback.

    Examples
    --------
    >>> import phantombunch as pb
    >>> pb.feedback()  # doctest: +SKIP
    ...

    """
    # Create a Faker generator
    fake = Faker()

    # Generate a random number between 1 and 3
    num_paragraphs = random.randint(nmin, nmax)

    # Generate the specified number of paragraphs
    random_paragraphs = fake.paragraphs(nb=num_paragraphs)

    # Join the paragraphs into a single string
    return "\n\n".join(random_paragraphs)

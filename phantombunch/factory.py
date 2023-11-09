from faker import Faker
import random
import pycountry
import phantombunch.util as util
import numpy as np

fake = Faker()



def cid():
    """Generate a random 8-digit CID number.

    The first digit is always 0, whereas the second digit is randomly 1 or 2. The remaining 6 digits are randomly generated between 0 and 9.

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

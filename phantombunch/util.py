from faker import Faker
import random


def cid():
    """Generate a random 8-digit CID number.
    
    The first digit is always 0, whereas the second digit is randomly 1 or 2. The remaining 6 digits are randomly generated between 0 and 9.

    """
    # The first digit is always 0.
    number = '0'
    # The second digit is randomly 1 or 2.
    number += str(random.choice([1, 2]))
    # Generate the remaining 6 digits randomly between 0 and 9.
    number += ''.join(str(random.randint(0, 9)) for _ in range(6))
    
    return number


def gender(values = ["male", "female", "nonbinary"],
           probabilities = [0.49, 0.5, 0.01]):
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


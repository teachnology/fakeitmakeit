import random


def cid():
    """Generate a random 8-digit CID number.
    
    The first digit is always 0, whereas the second digit is randomly 1 or 2. The remaining 6 digits are randomly generated between 0 and 9.

    """
    # The first digit is always 0
    number = '0'
    # The second digit is randomly 1 or 2
    number += str(random.choice([1, 2]))
    # Generate the remaining 6 digits randomly between 0 and 9
    for _ in range(6):
        number += str(random.randint(0, 9))
    return number

import pycountry
import faker


COUNTRIES = [country.name for country in pycountry.countries]
GENDERS = {"male": 0.49, "female": 0.5, "nonbinary": 0.01}


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

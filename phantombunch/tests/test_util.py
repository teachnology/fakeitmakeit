import numbers

import faker

import phantombunch.util as util


class TestCOUNTRIES:
    def test_type(self):
        # Check that COUNTRIES is a dictionary.
        assert isinstance(util.COUNTRIES, dict)

    def test_length(self):
        # Check that COUNTRIES has 249 countries.
        assert len(util.COUNTRIES) == 249

    def test_keys(self):
        # Check that the keys are country names.
        assert "Afghanistan" in util.COUNTRIES
        assert "Serbia" in util.COUNTRIES

    def test_values(self):
        # Check that the values are all 1 (relative probabilities).
        assert all(isinstance(value, numbers.Real) for value in util.COUNTRIES.values())


class TestGENDERS:
    def test_type(self):
        # Check that GENDERS is a dictionary.
        assert isinstance(util.GENDERS, dict)

    def test_length(self):
        # Check there are 3 genders.
        assert len(util.GENDERS) == 3

    def test_keys(self):
        # Check that the keys are genders.
        assert "male" in util.GENDERS

    def test_values(self):
        # Check that the values are all numbers.
        assert all(isinstance(value, numbers.Real) for value in util.GENDERS.values())


class TestLocale:
    def test_type(self):
        assert isinstance(util.locale("Germany"), str)
        assert util.locale("Serbia") is None

    def test_values(self):
        assert util.locale("United Kingdom") == "en_GB"
        assert util.locale("Serbia") is None

    def test_available_in_faker(self):
        possible_locales = [
            util.locale(country)
            for country in util.COUNTRIES
            if util.locale(country) is not None
        ]
        assert set(possible_locales) <= set(faker.config.AVAILABLE_LOCALES)
        assert len(possible_locales) == len(set(possible_locales))

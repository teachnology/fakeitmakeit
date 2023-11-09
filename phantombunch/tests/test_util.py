import numbers
import phantombunch.util as util
import faker


class TestCOUNTRIES:
    def test_type(self):
        assert isinstance(util.COUNTRIES, list)

    def test_length(self):
        assert len(util.COUNTRIES) == 249

    def test_values(self):
        assert "Afghanistan" in util.COUNTRIES
        assert "Serbia" in util.COUNTRIES


class TestGENDERS:
    def test_type(self):
        assert isinstance(util.GENDERS, dict)

    def test_length(self):
        assert len(util.GENDERS) == 3

    def test_keys(self):
        assert all(isinstance(key, str) for key in util.GENDERS.keys())
        assert "male" in util.GENDERS

    def test_values(self):
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

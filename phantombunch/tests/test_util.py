import numbers

import phantombunch.util as util


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


class TestCOURSES:
    def test_type(self):
        # Check that COURSES is a dictionary.
        assert isinstance(util.COURSES, dict)

    def test_keys(self):
        # Check that the keys are course names.
        assert "acse" in util.COURSES
        assert "edsml" in util.COURSES

    def test_values(self):
        # Check that the values are all numbers.
        assert all(isinstance(value, numbers.Real) for value in util.COURSES.values())


class TestTITLES:
    def test_type(self):
        # Check that TITLES is a list.
        assert isinstance(util.TITLES, list)

    def test_length(self):
        # Check that TITLES has 5 titles.
        assert len(util.TITLES) == 5

    def test_values(self):
        # Check that the values are all strings.
        assert all(isinstance(value, str) for value in util.TITLES)


class TestCOUNTRY_LOCALE:
    def test_type(self):
        # Check that COUNTRY_LOCALE is a dictionary.
        assert isinstance(util.COUNTRY_LOCALE, dict)

    def test_keys(self):
        # Check that the keys are country names.
        assert "Argentina" in util.COUNTRY_LOCALE
        assert "United States" in util.COUNTRY_LOCALE

    def test_values(self):
        # Check that the values contain an underscore.
        assert all("_" in value for value in util.COUNTRY_LOCALE.values())

    def test_entries(self):
        # Check that the entries are valid locales.
        assert util.COUNTRY_LOCALE["China"] == "zh_CN"
        assert util.COUNTRY_LOCALE["United Kingdom"] == "en_GB"


class TestDiscreteDraw:
    def test_output(self):
        # Check that the output is one of the expected ones.
        assert util.discrete_draw({"a": 0.5, "b": 0.5}) in {"a", "b"}


class TestValidEmail:
    def test_valid(self):
        # Check that valid emails are valid.
        assert util.valid_email("username@domain.com")
        assert util.valid_email("user.name@domain.com")
        assert util.valid_email("user_name@domain.ac.uk")

    def test_invalid(self):
        # Check that invalid emails are invalid.
        assert not util.valid_email("username@domain")
        assert not util.valid_email("user_name@domain.")
        assert not util.valid_email("user name@domain.com")

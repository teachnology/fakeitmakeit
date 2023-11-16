import numbers

import pytest

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


class TestValidUsername:
    def test_valid_usernames(self):
        # Test cases with valid usernames
        assert util.valid_username("s12")  # we allow one letter in username
        assert util.valid_username("ab12")
        assert util.valid_username("ab123")
        assert util.valid_username("abc1234")
        assert util.valid_username("xy9999")
        assert util.valid_username("x99999")  # we allow 5 digits in username

    def test_invalid_usernames_start_digit(self):
        # Test case with a username starting with a digit
        assert not util.valid_username("1ab123")

    def test_invalid_usernames_wrong_first_digit(self):
        # Test case with a username having '0' as the first digit after letters
        assert not util.valid_username("ab0234")

    def test_invalid_usernames_too_few_digits(self):
        # Test case with too few digits
        assert not util.valid_username("abc1")

    def test_invalid_usernames_too_many_digits(self):
        # Test case with too many digits
        assert not util.valid_username("ab123456")

    def test_invalid_usernames_uppercase_letters(self):
        # Test case with uppercase letters
        assert not util.valid_username("Abc123")

    def test_invalid_usernames_special_characters(self):
        # Test case with special characters
        assert not util.valid_username("ab#123")

    def test_invalid_usernames_too_many_letters(self):
        # Test case with too many letters
        assert not util.valid_username("abcd1234")

    def test_invalid_usernames_empty_string(self):
        # Test case with an empty string
        assert not util.valid_username("")


class TestValidCID:
    def test_valid_cid_basic(self):
        # Test valid CIDs that meet all the criteria
        assert util.valid_cid("01234567")
        assert util.valid_cid("02123456")
        assert util.valid_cid("00123456")  # we allow two leading zeroes

    def test_invalid_second_digit(self):
        # Test CIDs with an invalid second digit (should be 0, 1, or 2)
        assert not util.valid_cid("03123456")

    def test_invalid_length(self):
        # Test CIDs with incorrect length (should be exactly 8 digits)
        assert not util.valid_cid("0123456")  # Too short
        assert not util.valid_cid("012345678")  # Too long

    def test_invalid_starting_digit(self):
        # Test a CID that does not start with a digit
        assert not util.valid_cid("a1234567")

    def test_invalid_contains_non_digit(self):
        # Test CIDs that contain non-digit characters
        assert not util.valid_cid("01234a67")

    def test_invalid_empty_string(self):
        # Test an empty string (should be invalid)
        assert not util.valid_cid("")

    def test_invalid_special_characters(self):
        # Test CIDs that contain special characters
        assert not util.valid_cid("0123-567")


class TestValidName:
    def test_valid_single_word(self):
        # Test valid single word names (each word must start with a capital letter)
        assert util.valid_name("John")
        assert util.valid_name("Mary")

    def test_valid_multiple_words(self):
        # Test valid multiple word names (names with more than one word, each starting
        # with a capital letter)
        assert util.valid_name("John Smith")
        assert util.valid_name("Jean-Luc Picard")
        assert util.valid_name("Jean-Luc (Peter) Picard")

    def test_valid_hyphenated_names(self):
        # Test valid hyphenated names (names with hyphens, each part starting with a
        # capital letter)
        assert util.valid_name("Mary-Ann")
        assert util.valid_name("Jean-Paul")

    def test_invalid_capitalization(self):
        # Test names with invalid capitalization (names must start each word with a
        # capital letter)
        assert not util.valid_name("john")  # Not capitalized
        assert not util.valid_name("JOHN")  # All uppercase

    def test_invalid_contains_digits_or_characters(self):
        # Test names containing digits or special characters (names should only contain
        # letters, spaces, or hyphens)
        assert not util.valid_name("John123")  # Contains digits
        assert not util.valid_name("John@Doe")  # Contains special characters

    def test_invalid_use_of_hyphen_or_space(self):
        # Test names with incorrect use of hyphen or space (hyphens should replace
        # spaces, not be used alongside them)
        assert not util.valid_name("John - Smith")  # Hyphen not used correctly
        assert not util.valid_name("John  Smith")  # Double space

    def test_invalid_empty_or_whitespace(self):
        # Test empty string or names with leading/trailing whitespace (names should not
        # have extra whitespace)
        assert not util.valid_name("")  # Empty string
        assert not util.valid_name(" John")  # Leading space
        assert not util.valid_name("John ")  # Trailing space

    def test_parenthesis(self):
        # Test names with parenthesis.
        assert util.valid_name("John (Daniel) Smith")
        assert util.valid_name("John (Daniel)")


class TestValidTitle:
    @pytest.mark.parametrize(
        "title, expected",
        [
            ("Mr", True),  # Valid title
            ("Ms", True),  # Valid title
            ("Mrs", True),  # Valid title
            ("Mx", True),  # Valid title
            ("Miss", True),  # Valid title
            ("Dr", True),  # Valid title
            ("mr", False),  # Not correctly capitalized
            ("Doctor", False),  # Not an exact match
            ("Prof", False),  # Not in the list
            ("", False),  # Empty string
        ],
    )
    def test_valid_title(self, title, expected):
        assert util.valid_title(title) == expected


class TestValidCourse:
    @pytest.mark.parametrize(
        "course, expected",
        [
            ("acse", True),  # Valid course
            ("edsml", True),  # Valid course
            ("gems", True),  # Valid course
            ("ACSE", False),  # Not lowercase
            ("Edsml", False),  # Not lowercase
            ("gEmS", False),  # Not lowercase
            ("math", False),  # Not in the list
            ("", False),  # Empty string
        ],
    )
    def test_valid_course(self, course, expected):
        assert util.valid_course(course) == expected


class TestValidGender:
    @pytest.mark.parametrize(
        "gender, expected",
        [
            ("male", True),  # Valid gender
            ("female", True),  # Valid gender
            ("nonbinary", True),  # Valid gender
            ("Male", False),  # Not lowercase
            ("FEMALE", False),  # Not lowercase
            ("NonBinary", False),  # Not lowercase
            ("man", False),  # Not in the list
            ("woman", False),  # Not in the list
            ("", False),  # Empty string
        ],
    )
    def test_valid_gender(self, gender, expected):
        assert util.valid_gender(gender) == expected


class TestValidFeeStatus:
    @pytest.mark.parametrize(
        "fee_status, expected",
        [
            ("home", True),  # Valid fee status
            ("overseas", True),  # Valid fee status
            ("home - elq", True),  # Valid fee status
            ("Home", False),  # Not lowercase
            ("OVERSEAS", False),  # Not lowercase
            ("local", False),  # Not in the list
            ("international", False),  # Not in the list
            ("", False),  # Empty string
        ],
    )
    def test_valid_fee_status(self, fee_status, expected):
        assert util.valid_fee_status(fee_status) == expected

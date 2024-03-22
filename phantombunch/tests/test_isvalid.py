import pytest

import phantombunch as pb


class TestEmail:
    def test_valid(self):
        # Check that valid emails are valid.
        assert pb.isvalid.email("username@domain.com")
        assert pb.isvalid.email("user.name@domain.com")
        assert pb.isvalid.email("user_name@domain.ac.uk")

    def test_invalid(self):
        # Check that invalid emails are invalid.
        assert not pb.isvalid.email("username@domain")
        assert not pb.isvalid.email("user_name@domain.")
        assert not pb.isvalid.email("user name@domain.com")


class TestUsername:
    def test_valid_usernames(self):
        # Test cases with valid usernames
        assert pb.isvalid.username("s12")  # we allow one letter in username
        assert pb.isvalid.username("ab12")
        assert pb.isvalid.username("ab123")
        assert pb.isvalid.username("abc1234")
        assert pb.isvalid.username("xy9999")
        assert pb.isvalid.username("x99999")  # we allow 5 digits in username

    def test_invalid_usernames_start_digit(self):
        # Test case with a username starting with a digit
        assert not pb.isvalid.username("1ab123")

    def test_invalid_usernames_wrong_first_digit(self):
        # Test case with a username having '0' as the first digit after letters
        assert not pb.isvalid.username("ab0234")

    def test_invalid_usernames_too_few_digits(self):
        # Test case with too few digits
        assert not pb.isvalid.username("abc1")

    def test_invalid_usernames_too_many_digits(self):
        # Test case with too many digits
        assert not pb.isvalid.username("ab123456")

    def test_invalid_usernames_uppercase_letters(self):
        # Test case with uppercase letters
        assert not pb.isvalid.username("Abc123")

    def test_invalid_usernames_special_characters(self):
        # Test case with special characters
        assert not pb.isvalid.username("ab#123")

    def test_invalid_usernames_too_many_letters(self):
        # Test case with too many letters
        assert not pb.isvalid.username("abcd1234")

    def test_invalid_usernames_empty_string(self):
        # Test case with an empty string
        assert not pb.isvalid.username("")


class TestCID:
    def test_valid_cid_basic(self):
        # Test valid CIDs that meet all the criteria
        assert pb.isvalid.cid("01234567")
        assert pb.isvalid.cid("02123456")
        assert pb.isvalid.cid("00123456")  # we allow two leading zeroes

    def test_invalid_second_digit(self):
        # Test CIDs with an invalid second digit (should be 0, 1, or 2)
        assert not pb.isvalid.cid("03123456")

    def test_invalid_length(self):
        # Test CIDs with incorrect length (should be exactly 8 digits)
        assert not pb.isvalid.cid("0123456")  # Too short
        assert not pb.isvalid.cid("012345678")  # Too long

    def test_invalid_starting_digit(self):
        # Test a CID that does not start with a digit
        assert not pb.isvalid.cid("a1234567")

    def test_invalid_contains_non_digit(self):
        # Test CIDs that contain non-digit characters
        assert not pb.isvalid.cid("01234a67")

    def test_invalid_empty_string(self):
        # Test an empty string (should be invalid)
        assert not pb.isvalid.cid("")

    def test_invalid_special_characters(self):
        # Test CIDs that contain special characters
        assert not pb.isvalid.cid("0123-567")


class TestName:
    def test_valid_single_word(self):
        # Test valid single word names (each word must start with a capital letter)
        assert pb.isvalid.name("John")
        assert pb.isvalid.name("Mary")

    def test_valid_multiple_words(self):
        # Test valid multiple word names (names with more than one word, each starting
        # with a capital letter)
        assert pb.isvalid.name("John Smith")
        assert pb.isvalid.name("Jean-Luc Picard")
        assert pb.isvalid.name("Jean-Luc (Peter) Picard")

    def test_valid_hyphenated_names(self):
        # Test valid hyphenated names (names with hyphens, each part starting with a
        # capital letter)
        assert pb.isvalid.name("Mary-Ann")
        assert pb.isvalid.name("Jean-Paul")

    def test_invalid_capitalization(self):
        # Test names with invalid capitalization (names must start each word with a
        # capital letter)
        assert not pb.isvalid.name("john")  # Not capitalized
        assert not pb.isvalid.name("JOHN")  # All uppercase

    def test_invalid_contains_digits_or_characters(self):
        # Test names containing digits or special characters (names should only contain
        # letters, spaces, or hyphens)
        assert not pb.isvalid.name("John123")  # Contains digits
        assert not pb.isvalid.name("John@Doe")  # Contains special characters

    def test_invalid_use_of_hyphen_or_space(self):
        # Test names with incorrect use of hyphen or space (hyphens should replace
        # spaces, not be used alongside them)
        assert not pb.isvalid.name("John - Smith")  # Hyphen not used correctly
        assert not pb.isvalid.name("John  Smith")  # Double space

    def test_invalid_empty_or_whitespace(self):
        # Test empty string or names with leading/trailing whitespace (names should not
        # have extra whitespace)
        assert not pb.isvalid.name("")  # Empty string
        assert not pb.isvalid.name(" John")  # Leading space
        assert not pb.isvalid.name("John ")  # Trailing space

    def test_parenthesis(self):
        # Test names with parenthesis.
        assert pb.isvalid.name("John (Daniel) Smith")
        assert pb.isvalid.name("John (Daniel)")


class TestTitle:
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
        assert pb.isvalid.title(title) == expected


class TestCourse:
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
        assert pb.isvalid.course(course) == expected


class TestGender:
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
        assert pb.isvalid.gender(gender) == expected


class TesteeStatus:
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
        assert pb.isvalid.fee_status(fee_status) == expected

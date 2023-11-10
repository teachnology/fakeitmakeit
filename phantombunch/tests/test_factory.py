import collections
import re

import pytest

import phantombunch as pb
import phantombunch.util as pbu

UINT_RE = re.compile(r"^[0-9]+$")  # unsigned integer regex


class TestCID:
    def test_type(self):
        # Check that the CID is a string.
        assert isinstance(pb.cid(), str)

    def test_length(self):
        # Check that the CID is 8 digits long.
        assert len(pb.cid()) == 8

    def test_all_digits(self):
        # Check that the CID is all digits.
        assert UINT_RE.search(pb.cid())

    def test_first_digit(self):
        # Check that the first digit is always 0.
        assert int(pb.cid()[0]) == 0

    def test_second_digit(self):
        # Check that the second digit is always 1 or 2.
        assert int(pb.cid()[1]) in [1, 2]

    def test_remaining_digits(self):
        # Check that the remaining 6 digits are always between 0 and 9.
        assert UINT_RE.search(pb.cid()[2:])

    def test_all_digits_present(self):
        # Check that all digits (0-9) can be present in the CID.
        assert len(set("".join(pb.cid() for _ in range(50)))) == 10

    def test_convertible(self):
        # Check that the CID is convertible to an integer.
        assert isinstance(int(pb.cid()), int)


class TestGender:
    def test_type(self):
        # Check that gender is a string.
        assert isinstance(pb.gender(), str)

    def test_values(self):
        # Check the output is one of the expected ones.
        assert pb.gender() in pbu.GENDERS

    def test_probability_certain_outcome(self):
        # Check that the probabilities are respected.
        assert pb.gender(distribution={"outcome1": 1, "outcome2": 0}) == "outcome1"

    def test_probabilities_uncertain_outcome(self):
        # Check that the probabilities are respected.
        distribution = {"male": 0.2, "female": 0.75, "nonbinary": 0.05}
        counts = collections.Counter(
            pb.gender(distribution=distribution) for _ in range(1000)
        )
        assert counts["nonbinary"] < counts["male"] < counts["female"]


class TestTitle:
    def test_type(self):
        # Check that title is a string.
        assert isinstance(pb.title(), str)

    def test_use_period(self):
        # Check that the title ends with a period if use_period is True.
        assert pb.title(use_period=True).endswith(".")

    def test_no_period(self):
        # Check that the title does not end with a period if use_period is False.
        assert not pb.title(use_period=False).endswith(".")

    def test_startswith_upper(self):
        # Check that the title starts with an uppercase M.
        assert pb.title().startswith("M")

    def test_no_gender(self):
        # Check that the title is one of the expected ones.
        assert pb.title() in pbu.TITLES

    def test_male(self):
        # Check that the title is one of the expected ones for a male.
        assert pb.title(genderval="male") == "Mr"

    def test_female(self):
        # Check that the title is one of the expected ones for a female.
        assert pb.title(genderval="female") in ["Ms", "Mrs", "Miss"]

    def test_nonbinary(self):
        # Check that the title is one of the expected ones for a nonbinary.
        assert pb.title(genderval="nonbinary") == "Mx"

    def test_wrong_gender(self):
        # Check the exception is raised.
        with pytest.raises(ValueError):
            pb.title(genderval="wrong")


class TestCourse:
    def test_type(self):
        # Check that course is a string.
        assert isinstance(pb.course(), str)

    def test_values(self):
        # Check the output is one of the expected ones.
        assert pb.course() in pbu.COURSES

    def test_probability_certain_outcome(self):
        # Check that the probabilities are respected.
        assert pb.course(distribution={"course1": 1, "course2": 0}) == "course1"

    def test_probabilities_uncertain_outcome(self):
        # Check that the probabilities are respected.
        distribution = {"c1": 0.2, "c2": 0.75, "c3": 0.05}
        counts = collections.Counter(
            pb.course(distribution=distribution) for _ in range(1000)
        )
        assert counts["c3"] < counts["c1"] < counts["c2"]


class TestCountry:
    def test_type(self):
        # Check that country is a string.
        assert isinstance(pb.country(), str)

    def test_defaults(self):
        # Check that the country is one of the expected ones.
        assert pb.country() in pbu.COUNTRIES

    def test_probability_certain_outcome(self):
        # Check that the probabilities are respected.
        assert pb.country(distribution={"country1": 1, "country2": 0}) == "country1"

    def test_probabilities_uncertain_outcome(self):
        # Check that the probabilities are respected.
        distribution = {"c1": 0.2, "c2": 0.75, "c3": 0.05}
        counts = collections.Counter(
            pb.country(distribution=distribution) for _ in range(1000)
        )
        assert counts["c3"] < counts["c1"] < counts["c2"]

    def test_bias(self):
        # Check that the bias is respected.
        bias = {"China": 1000, "United Kingdom": 100}
        counts = collections.Counter(pb.country(bias=bias) for _ in range(100))
        assert counts["China"] > counts["United Kingdom"] > counts["Syria"]


class TestUsername:
    def test_type(self):
        # Check that username is a string.
        assert isinstance(pb.username(), str)

    def test_length(self):
        # Check that the username is between 4 and 7 characters long.
        assert 4 <= len(pb.username()) <= 7

    def test_lower(self):
        # Check that the username is lowercase.
        assert pb.username().islower()

    def test_no_space(self):
        # Check that the username does not contain spaces.
        assert " " not in pb.username()

    def test_first_letter(self):
        # Check that the first letter is the first letter of the first name.
        assert pb.username(nameval="John Smith").startswith("j")

    def test_last_letter(self):
        # Check that the last letter is the first letter of the last name.
        letters = [i for i in pb.username(nameval="John Doe") if i.isalpha()]
        assert letters[-1] == "d"

    def test_num_digits(self):
        # Check that the username contains 2 to 4 digits.
        assert 2 <= sum(i.isdigit() for i in pb.username()) <= 4

    def test_num_letters(self):
        # Check that the username contains 2 or 3 letters.
        assert 2 <= sum(i.isalpha() for i in pb.username()) <= 3


class TestEmail:
    def test_type(self):
        # Check that email is a string.
        assert isinstance(pb.email(), str)

    def test_at(self):
        # Check that the email contains an @.
        assert "@" in pb.email()

    def test_dot(self):
        # Check that the email contains a dot.
        assert "." in pb.email()

    def test_domain(self):
        # Check that the email contains the domain if specified.
        assert pb.email(domain="gmail.com").endswith("@gmail.com")

    def test_valid(self):
        # Check that the email is valid.
        assert pbu.valid_email(pb.email())


class TestTutor:
    pass

class TestName:
    def test_type(self):
        assert isinstance(pb.name(), str)

    def test_space(self):
        assert " " in pb.name()

    def test_country_gender(self):
        for _ in range(25):
            assert isinstance(pb.name(gender=pb.gender(), country=pb.country()), str)

    def test_china(self):
        names = set(" ".join(pb.name(country="China") for _ in range(100)).split())
        assert len({"Jang", "Jing", "Wei", "Fang", "Lei", "Tao"} & names) > 0

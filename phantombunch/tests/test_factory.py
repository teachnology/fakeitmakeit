import collections
import re

import numpy as np
import pandas as pd
import pytest

import phantombunch as pb
import phantombunch.util as pbu

UINT_RE = re.compile(r"^[0-9]+$")  # unsigned integer regex


@pytest.fixture(scope="package")
def cohort():
    return pb.cohort(100)


@pytest.fixture(scope="package")
def assignment(cohort):
    return pb.assignment(cohort["username"], feedback=True)


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
        assert pb.isvalid.email(pb.email())


class TestName:
    def test_type(self):
        # Check that name is a string.
        assert isinstance(pb.name(), str)

    def test_space(self):
        # Check that the name contains a space.
        assert " " in pb.name()

    def test_country_gender(self):
        # Check that different countries and names are accepted.
        assert all(
            isinstance(pb.name(genderval=pb.gender(), countryval=pb.country()), str)
            for _ in range(25)
        )

    def test_china(self):
        # Check that Chinese names are generated as expected.
        names = set(" ".join(pb.name(countryval="China") for _ in range(100)).split())
        assert {"Jang", "Jing", "Wei", "Fang", "Lei", "Tao"} & names

    def test_gender(self):
        # Check expected female names are in the output.
        names = set(
            " ".join(
                pb.name(genderval="female", countryval="United Kingdom")
                for _ in range(100)
            ).split()
        )
        assert {"Ellie", "Jill", "Irene", "Jean", "Megan", "Fiona", "Sylvia"} & names


class TestMark:
    def test_type(self):
        # Check that mark is a float.
        assert isinstance(pb.mark(), float)

    def test_range(self):
        # Check that the mark is between 0 and 100.
        assert 0 <= pb.mark() <= 100

    def test_fail_probability_1(self):
        # Check fail_probability is respected.
        assert pb.mark(fail_probability=1) == 0.0

    def test_fail_probability_0_5(self):
        # Check fail_probability is respected.
        marks = np.array([pb.mark(fail_probability=0.5) for _ in range(100)])
        assert 35 <= len(marks[marks == 0]) <= 65

    def test_fail_probability_0(self):
        # Check fail_probability is respected.
        marks = np.array([pb.mark(fail_probability=0) for _ in range(100)])
        assert len(marks[marks == 0]) == 0

    def test_mean(self):
        # Check that the mean is as expected.
        marks = np.array(
            [pb.mark(mean=65, stdev=10, fail_probability=0) for _ in range(100)]
        )
        assert 60 <= marks.mean() <= 70

    def test_sd(self):
        # Check that the standard deviation is as expected.
        marks = np.array(
            [pb.mark(mean=65, stdev=10, fail_probability=0) for _ in range(100)]
        )
        assert 8 <= marks.std() <= 12


class TestStudent:
    def test_type(self):
        # Check that the output is a Student dataclass.
        assert isinstance(pb.student(), pb.Student)

    def test_cid(self):
        # Check that the CID is a string.
        assert hasattr(pb.student(), "cid")

    def test_repr(self):
        # Check that the repr string makes sense.
        assert "Student" in repr(pb.student())


class TestCohort:
    def test_type(self, cohort):
        # Check that the output is a DataFrame.
        assert isinstance(cohort, pd.DataFrame)

    def test_course(self, cohort):
        # Check that the output is the right length.
        assert len(cohort["course"].unique()) == 3

    def test_tutor(self, cohort):
        # Check that the number of tutors is bounded.
        assert len(cohort["tutor"].unique()) <= 25

    def test_nationality(self, cohort):
        # Check that nationalities are as expected.
        counts = collections.Counter(cohort["nationality"])

        assert set(counts.keys()) <= set(pb.util.COUNTRIES.keys())
        assert counts["China"] > 40
        assert counts["United Kingdom"] > 4

    def test_username(self, cohort):
        # Check that usernames are as expected.
        assert cohort["username"].map(pb.isvalid.username).all()

    def test_cid(self, cohort):
        # Check that CIDs are as expected.
        assert cohort["cid"].map(pb.isvalid.cid).all()

    def test_email(self, cohort):
        # Check that emails are as expected.
        assert cohort["email"].map(pb.isvalid.email).all()

    def test_personal_email(self, cohort):
        # Check that emails are as expected.
        assert cohort["personal_email"].map(pb.isvalid.email).all()

    def test_title(self, cohort):
        # Check that titles are as expected.
        assert cohort["title"].map(pb.isvalid.title).all()

    def test_first_name(self, cohort):
        # Check that names are as expected.
        assert cohort["first_name"].map(pb.isvalid.name).all()

    def test_last_name(self, cohort):
        # Check that names are as expected.
        assert cohort["last_name"].map(pb.isvalid.name).all()

    def test_gender(self, cohort):
        # Check that genders are as expected.
        assert cohort["gender"].map(pb.isvalid.gender).all()

    def test_fee_status(self, cohort):
        # Check that genders are as expected.
        assert cohort["fee_status"].map(pb.isvalid.fee_status).all()


class TestAssignment:
    def test_type(self, assignment):
        # Check that the output is a DataFrame.
        assert isinstance(assignment, pd.DataFrame)

    def test_columns(self, assignment):
        # Check that the output has the right columns.
        assert set(assignment.columns) == set(["username", "mark", "feedback"])

    def test_username(self, cohort, assignment):
        # Check that the usernames are as expected.
        assert set(assignment["username"]) == set(cohort["username"])

    def test_mark(self, assignment):
        # Check that the marks are as expected.
        assert assignment["mark"].between(0, 100).all()

    def test_feedback(self, assignment):
        # Check that the feedback is as expected.
        assert assignment["feedback"].str.len().ge(10).all()

    def test_no_feedback(self, cohort):
        # Check that the feedback is as expected.
        assignment = pb.assignment(cohort["username"], feedback=False)
        assert "feedback" not in assignment.columns

    def test_isvalid(self, cohort):
        # Check that the output is a DataFrame.
        assignment = pb.assignment(cohort["username"], feedback=True)
        assert pb.isvalid.assignment(assignment, valid_cohort=cohort)


class TestValidCohort:
    def test_valid_cohort(self, cohort):
        # Check that the output is a DataFrame.
        assert pb.isvalid.cohort(cohort)

    def test_invalid_cohort(self, cohort):
        # Check that the output is a DataFrame.
        cohort["username"] = cohort["username"] + "#"
        assert not pb.isvalid.cohort(cohort)

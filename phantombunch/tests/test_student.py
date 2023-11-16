import collections

import pandas as pd
import pytest

import phantombunch as pb


@pytest.fixture(scope="module")
def cohort():
    return pb.cohort(100)


@pytest.fixture(scope="module")
def assignment(cohort):
    return pb.assignment(cohort["username"], feedback=True)


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
    # def setup_method(self):
    #     # Create a cohort of 10 students.
    #     self.cohort = pb.cohort(100)

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
        assert counts["United Kingdom"] > 5

    def test_username(self, cohort):
        # Check that usernames are as expected.
        assert cohort["username"].map(pb.util.valid_username).all()

    def test_cid(self, cohort):
        # Check that CIDs are as expected.
        assert cohort["cid"].map(pb.util.valid_cid).all()

    def test_email(self, cohort):
        # Check that emails are as expected.
        assert cohort["email"].map(pb.util.valid_email).all()

    def test_personal_email(self, cohort):
        # Check that emails are as expected.
        assert cohort["personal_email"].map(pb.util.valid_email).all()

    def test_title(self, cohort):
        # Check that titles are as expected.
        assert cohort["title"].map(pb.util.valid_title).all()

    def test_first_name(self, cohort):
        # Check that names are as expected.
        assert cohort["first_name"].map(pb.util.valid_name).all()

    def test_last_name(self, cohort):
        # Check that names are as expected.
        assert cohort["last_name"].map(pb.util.valid_name).all()

    def test_gender(self, cohort):
        # Check that genders are as expected.
        assert cohort["gender"].map(pb.util.valid_gender).all()

    def test_fee_status(self, cohort):
        # Check that genders are as expected.
        assert cohort["fee_status"].map(pb.util.valid_fee_status).all()


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

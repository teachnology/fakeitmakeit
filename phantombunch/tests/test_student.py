import collections

import pandas as pd

import phantombunch as pb


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
    def setup_method(self):
        # Create a cohort of 10 students.
        self.cohort = pb.cohort(100)

    def test_type(self):
        # Check that the output is a DataFrame.
        assert isinstance(self.cohort, pd.DataFrame)

    def test_course(self):
        # Check that the output is the right length.
        assert len(self.cohort["course"].unique()) == 3

    def test_tutor(self):
        # Check that the number of tutors is bounded.
        assert len(self.cohort["tutor"].unique()) <= 25

    def test_fee_status(self):
        # Check that the number of fee statuses is bounded.
        assert len(self.cohort["fee_status"].unique()) <= 2

    def test_nationality(self):
        # Check that nationalities are as expected.
        counts = collections.Counter(self.cohort["nationality"])

        assert set(counts.keys()) <= set(pb.util.COUNTRIES.keys())
        assert counts["China"] > 40
        assert counts["United Kingdom"] > 5

    def test_gender(self):
        # Check that genders are as expected.
        counts = collections.Counter(self.cohort["gender"])

        assert set(counts.keys()) <= set(pb.util.GENDERS.keys())
        assert counts["male"] > counts["female"]


class TestAssignment:
    def setup_method(self):
        # Create a cohort and an assignment with 100 students.
        self.cohort = pb.cohort(100)
        self.assignment = pb.assignment(self.cohort["username"], feedback=True)

    def test_type(self):
        # Check that the output is a DataFrame.
        assert isinstance(self.assignment, pd.DataFrame)

    def test_columns(self):
        # Check that the output has the right columns.
        assert set(self.assignment.columns) == set(["username", "mark", "feedback"])

    def test_username(self):
        # Check that the usernames are as expected.
        assert set(self.assignment["username"]) == set(self.cohort["username"])

    def test_mark(self):
        # Check that the marks are as expected.
        assert self.assignment["mark"].between(0, 100).all()

    def test_feedback(self):
        # Check that the feedback is as expected.
        assert self.assignment["feedback"].str.len().ge(10).all()

    def test_no_feedback(self):
        # Check that the feedback is as expected.
        assignment = pb.assignment(self.cohort["username"], feedback=False)
        assert "feedback" not in assignment.columns

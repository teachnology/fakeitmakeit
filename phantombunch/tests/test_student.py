import phantombunch as pb
import pandas as pd
import collections


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

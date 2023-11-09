import phantombunch as pb
import pandas as pd


class TestCohort:
    def test_type(self):
        assert isinstance(pb.cohort(10), pd.DataFrame)

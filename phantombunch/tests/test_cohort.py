import pandas as pd

import phantombunch as pb


class TestCohort:
    def test_type(self):
        assert isinstance(pb.cohort(10), pd.DataFrame)

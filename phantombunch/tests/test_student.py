import phantombunch as pb


class TestStudent:
    def test_type(self):
        assert isinstance(pb.student(), pb.Student)

    def test_cid(self):
        assert hasattr(pb.student(), "cid")

    def test_repr(self):
        assert "Student" in repr(pb.student())

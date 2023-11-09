import re
import phantombunch as pb
import collections

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
        assert all(pb.cid()[0] for _ in range(100))

    def test_second_digit(self):
        # Check that the second digit is always 1 or 2.
        assert all(pb.cid()[1] in ["1", "2"] for _ in range(100))

    def test_remaining_digits(self):
        # Check that the remaining 6 digits are always between 0 and 9.
        digits_0_to_9 = [str(i) for i in range(10)]
        assert all(i in digits_0_to_9 for i in pb.cid()[2:] for _ in range(100))

    def test_all_digits_present(self):
        # Check that all digits (0-9) can be present in the CID.
        assert len(set("".join(pb.cid() for _ in range(100)))) == 10


class TestGender:
    def test_type(self):
        assert isinstance(pb.gender(), str)

    def test_values(self):
        assert pb.gender() in pb.GENDERS

    def test_probabilities(self):
        # Check that the probabilities are respected.
        probabilities = [0.2, 0.75, 0.05]
        genders = [pb.gender(probabilities=probabilities) for _ in range(10000)]
        counts = collections.Counter(genders)
        assert counts["nonbinary"] < counts["male"] < counts["female"]


class TestCountry:
    def test_type(self):
        assert isinstance(pb.country(), str)

    def test_values(self):
        assert pb.country() in pb.COUNTRIES

    def test_bias(self):
        bias = {"China": 0.5, "United Kingdom": 0.2}
        countries = [pb.country(bias=bias) for _ in range(100)]
        counts = collections.Counter(countries)
        assert counts["China"] > counts["United Kingdom"] > counts["Croatia"]
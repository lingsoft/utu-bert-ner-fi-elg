import unittest
import os

from utils import iob2_to_elg


def read_fixture(fname):
    fixture_path = "tests/unit/fixtures/"
    with open(os.path.join(fixture_path, fname)) as infile:
        return infile.read()


class TestTagConversion(unittest.TestCase):

    def setUp(self):
        self.steady_text = read_fixture("steady_text.txt")
        self.steady_ner = read_fixture("steady_ner.tsv")
        self.steady_expected = eval(read_fixture("steady_expected.txt"))
        self.tag_change_text = read_fixture("tag_change_text.txt")
        self.tag_change_ner = read_fixture("tag_change_ner.tsv")
        self.tag_change_expected = eval(read_fixture(
            "tag_change_expected.txt"))

    def test_iob2_to_elg_with_steady_text(self):
        """Return three entities"""
        result = iob2_to_elg(self.steady_text, self.steady_ner)
        self.assertCountEqual(result, self.steady_expected)

    def test_iob2_to_elg_with_tag_change(self):
        """Return two entities"""
        result = iob2_to_elg(self.tag_change_text, self.tag_change_ner)
        self.assertCountEqual(result, self.tag_change_expected)


if __name__ == '__main__':
    unittest.main()

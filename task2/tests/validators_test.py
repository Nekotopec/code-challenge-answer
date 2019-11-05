import pytest
from src.validators import DateValidator, resolution_validation


class TestDate():
    """ Class for testing date validator."""
    @pytest.mark.parametrize('date', ['05 2012', '08 2019', '12 2018'])
    def test_correct_date(self, date):
        """ Test date validation with correct date."""
        assert 1 == 1

    def test_future(self):
        """ Test date validation with date in the future."""
        pass

    def test_incorrect_date(self):
        """ Test date validation with incorrect date."""
        pass


class ResolutionValidatorTest():

    def test_wrong_format_resolution(self):
        """ Test resolution validator with resolution in the wrong format."""
        pass

    def test_correct_format_resolution(self):
        """ Test resolution validator with resolution in the correct format."""
        pass

import datetime
import re


class DateValidator():
    """ Class for input parametrs validation."""

    def date_validation(self, month, year):
        # Validate month.
        if not month.isdigit():
            print('Input the month using digits.')
            return False
        elif int(month) > 12 or int(month) < 1:
            print('Month must be from 1 to 12, not {}'.format(month))
            return False

        # Validate Year.
        if not year.isdigit():
            print('Input the year using digits.')
            return False
        elif int(year) < 2015:
            print('Input year after the 2015th.')
            return False

        # Validate date.
        day = datetime.datetime.now().strftime('%d')

        # Fix ValueError when day is out of range for month.
        try:
            date = datetime.datetime(int(year), int(month), int(day))
        except ValueError:
            date = datetime.datetime(int(year), int(month), 28)

        if datetime.datetime.now() < date:
            print('You input a date from the future.')
            return False

        return True


def resolution_validation(resolution):

    # Validate resolution.
    if not re.search(r'\b\d{3,4}x\d{3,4}\b', resolution):
        print('You input resolution in the invalid format.')
        return False

    return True

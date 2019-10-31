import sys
import os
import datetime
import re
import requests

from bs4 import BeautifulSoup


class Validator():
    """ Class for input parametrs validation."""

    def validation(self, month, year, resolution):

        if not _date_validation(month, year):
            return False

        if not _resolution_validation(resolution):
            return False

        return True

    def _date_validation(self, month, year):
        # Validate month.
        if not month.isdigit():
            print('Input the month using digits.'.)
            return False
        elif int(month) > 12 or int(month) < 1:
            print('Month must be from 1 to 12.')
            return False

        # Validate Year.
        if not year.isdigit():
            print('Input the year using digits.'.)
            return False
        elif int(year) < 2015:
            print('Input year after the 2015th.')
            return False
        day = datetime.datetime.now().strftime('%d')

        # Validate date.
        if datetime.datetime.now() < datetime.datetime(int(year), int(month), day):
            print('You input a date from the future.')
            return False

        return True

    def _resolution_validation(self, resolution):

        # Validate resolution.
        if not re.search(r'\b\d{3,4}x\d{3,4}\b', resolution):
            print('You input resolution in the invalid format.')
            return False

        return True


class PageGetter():
    """ Class for getting page."""

    def get_page(self, month, year):
        """ Get page.text with requests"""
        url = _url_getter(month, year)

    def _url_getter(self, month, year):
        year_number = int(year)
        month_number = int(month)
        if month_number == 1:
            month_before_number = 12
            year_before_number = year_number - 1
        else:
            month_before_number = month_number - 1
            year_before_number = year_number
        month_before_number = datetime.datetime(year_before_number,month_before_number,1).strftime('%m')
        month_name = datetime.datetime(year_number,month_number,1).strftime('%B').lower()
        url = f'https://www.smashingmagazine.com/{year_before_number}/{04}/desktop-wallpaper-calendars-{may}-{year_number}/'


if __name__ == "__main__":
    month, year, resolution = sys.argv[1:4]
    validator = Validator()
    if validator.validation(month, year, resolution):
        page_getter = PageGetter()
        page = page_getter.get_page(month, year)
        page_parser = PageParser(page)
        name_link_dict = page_parser.get_wallpaper(resolution)
        path = './Wallpapers'
        if not os.path.isdir(path):
            os.mkdir(path)
        saver = Saver()
        saver.save_wallpapers(name_link_dict)
    else:
        print('''Input parametrs shuold be like \n
                 python3 task2.py 2017 05 1920x1080''')

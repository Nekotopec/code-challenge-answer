import sys
import os
import datetime
import re

import requests
from bs4 import BeautifulSoup


class Validator():
    """ Class for input parametrs validation."""

    def validation(self, month, year, resolution):

        if not self._date_validation(month, year):
            return False

        if not self._resolution_validation(resolution):
            return False

        return True

    def _date_validation(self, month, year):
        # Validate month.
        if not month.isdigit():
            print('Input the month using digits.')
            return False
        elif int(month) > 12 or int(month) < 1:
            print(int(month))
            print('Month must be from 1 to 12.')
            return False

        # Validate Year.
        if not year.isdigit():
            print('Input the year using digits.')
            return False
        elif int(year) < 2015:
            print('Input year after the 2015th.')
            return False
        day = datetime.datetime.now().strftime('%d')

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
        url = self._url_getter(month, year)
        page = requests.get(url).text

        return page

    def _url_getter(self, month, year):
        year_number = int(year)
        month_number = int(month)
        if month_number == 1:
            month_before_number = 12
            year_before_number = year_number - 1
        else:
            month_before_number = month_number - 1
            year_before_number = year_number

        # Get month as a zero-padded decimal number.
        month_before_number = datetime.datetime(
            year_before_number, month_before_number, 1).strftime('%m')

        # Get month name
        month_name = datetime.datetime(year_number, month_number, 1).strftime('%B').lower()

        url = f'https://www.smashingmagazine.com/{year_before_number}/{month_before_number}/desktop-wallpaper-calendars-{month_name}-{year_number}/'

        return url


class PageParser():
    """ Class for parsing the page."""

    def __init__(self, page):
        self.page = page
        self.soup = self._get_soup()
        self.content = self._get_content()

    def _get_soup(self):
        soup = BeautifulSoup(self.page, "lxml")
        return soup

    def _get_content(self):
        content = self.soup.find(id='article__content')
        return content

    def find_all_wallpapers(self, resolution):
        """ Method that find all wallpapers with desired resolution."""
        # compile regexp for future search
        reg = re.compile(r'([\w ?!°-]+)- \b\d{3,4}x\d{3,4}\b')
        name_link_dict = dict()
        content_feature_panel = self.content.find_next(class_='feature-panel-container')
        figure = content_feature_panel.find_next('figure')
        while figure:
            ul = figure.find_next('ul')
            li = ul.find_all('li')[2]
            for a in li.find_all('a'):
                if resolution in a['title']:
                    key = reg.search(a['title']).group(1)
                    name_link_dict[key] = a['href']
            figure = figure.find_next('figure')
        return name_link_dict


class Saver():
    """ Class for saving wallpapers."""

    def __init__(self, path):
        self.path = path

    def save_wallpapers(self, name_link_dict):
        for key, value in name_link_dict.items():
            image = requests.get(value)
            if image.status_code == 200:
                filename = os.path.join(self.path, key)
                with open(f'{filename}.jpg'.format(key), 'wb') as f:
                    f.write(image.content)


if __name__ == "__main__":

    WARNING = 'Input parametrs shuold be like\n\'python3 task2.py 05 2017 1920x1080\'.'

    if len(sys.argv) == 4:
        month, year, resolution = sys.argv[1:4]
        validator = Validator()
        if validator.validation(month, year, resolution):
            page_getter = PageGetter()
            page = page_getter.get_page(month, year)
            page_parser = PageParser(page)
            name_link_dict = page_parser.find_all_wallpapers(resolution)
            if len(name_link_dict) < 1:
                print('You picked a wrong resolution.')
            path = './Wallpapers'
            if not os.path.isdir(path):
                os.mkdir(path)
            saver = Saver(path)
            saver.save_wallpapers(name_link_dict)
        else:
            print(WARNING)
    else:
        print(WARNING)

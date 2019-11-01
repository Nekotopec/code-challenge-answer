import datetime
import re

import requests
from bs4 import BeautifulSoup


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
            year_before_number, month_before_number, 1,
        ).strftime('%m')

        # Get month name
        month_name = datetime.datetime(
            year_number, month_number, 1,
        ).strftime('%B').lower()

        url = ('https://www.smashingmagazine.com/'
               f'{year_before_number}/{month_before_number}/'
               f'desktop-wallpaper-calendars-{month_name}-{year_number}/')

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
        content_feature_panel = self.content.find_next(
            class_='feature-panel-container')
        figure = content_feature_panel.find_next('figure')
        while figure:
            ul = figure.find_next('ul')

            li = ul.find_all('li')[-1]
            for a in li.find_all('a'):
                if resolution in a['title']:
                    key = reg.search(a['title']).group(1)
                    name_link_dict[key] = a['href']
            figure = figure.find_next('figure')
        return name_link_dict

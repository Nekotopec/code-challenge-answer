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
        # Counter for nameless wallpapers
        counter_of_nameless = 1

        # Get resolution parametrs
        res_h, res_w = re.search(r'(\d{3,4})x(\d{3,4})',
                                 resolution).group(1, 2)

        # Compile regexp for future search
        reg = re.compile(r'([\w ?!°-]+)- \b\d{3,4}x\d{3,4}\b')

        name_link_dict = dict()
        content_feature_panel = self.content.find_next(
            class_='feature-panel-container')
        figure = content_feature_panel.find_next('figure')
        while figure:
            ul = figure.find_next('ul')

            li = ul.find_all('li')[-1]
            for a in li.find_all('a'):
                if res_h in a.text and res_w in a.text:

                    # Some Walls haven't Titles
                    if a.get('title'):
                        key = reg.search(a['title']).group(1)
                    else:
                        key = f'without_name{counter_of_nameless}'
                        counter_of_nameless += 1

                    name_link_dict[key] = a['href']
            figure = figure.find_next('figure')
        return name_link_dict

import sys
import os


from page import PageGetter, PageParser
from validators import DateValidator, resolution_validation
from saver import Saver


if __name__ == "__main__":

    WARNING = ('Input parametrs shuold be like\n\'python3 '
               'main.py 05 2017 1920x1080\'.')

    if len(sys.argv) == 4:
        month, year, resolution = sys.argv[1:4]
        validator = DateValidator()
        if (validator.date_validation(month, year) and
                resolution_validation(resolution)):
            page_getter = PageGetter()
            page = page_getter.get_page(month, year)
            page_parser = PageParser(page)
            name_link_dict = page_parser.find_all_wallpapers(resolution)
            if len(name_link_dict) < 1:
                print('You picked a wrong resolution.')
            base_dir = os.path.dirname(__file__)
            wall_dir = os.path.dirname(base_dir)
            path = os.path.join(wall_dir, 'Wallpapers')
            if not os.path.isdir(path):
                os.mkdir(path)
            saver = Saver(path)
            saver.save_wallpapers(name_link_dict)
        else:
            print(WARNING)
    else:
        print(WARNING)

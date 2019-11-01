import requests
import os


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

import configparser
import time

from whatsapp_scrapper import WhatsappScrapper


def load_settings():
    """
    Loading and assigning global variables from our settings.txt file
    """
    config_parser = configparser.RawConfigParser()
    config_file_path = 'mysettings.txt'
    config_parser.read(config_file_path)

    browser = config_parser.get('config', 'BROWSER')
    browser_path = config_parser.get('config', 'BROWSER_PATH')
    name = config_parser.get('config', 'NAME')
    page = config_parser.get('config', 'PAGE')

    settings = {
        'browser': browser,
        'browser_path': browser_path,
        'name': name,
        'page': page
    }
    return settings


def main():
    """
    Loading all the configuration and opening the website
    (Browser profile where whatsapp web is already scanned)
    """
    settings = load_settings()
    scrapper = WhatsappScrapper(
        settings['page'], settings['browser'], settings['browser_path'])

    time.sleep(5)

    if scrapper.open_conversation(settings['name']):
        scrapper.scroll_n_save(2)


if __name__ == '__main__':
    main()

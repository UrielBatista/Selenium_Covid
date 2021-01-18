from selenium.common.exceptions import NoSuchElementException
from time import sleep
from scraping import Scraping

if __name__ == '__main__':
    try:
        scraping = Scraping()
        scraping.scrap_and_insert()
        sleep(1)
        print('The And!!')

    except Exception as exception:
        print(exception)

    finally:
        pass




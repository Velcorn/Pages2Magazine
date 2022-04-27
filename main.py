import os
import re
import shutil
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from tqdm import tqdm
from config import login_config


email = login_config()['email']
password = login_config()['password']


def main():
    # Set Chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-gpu')

    # Create and set download directory
    downloads = r"D:\Programming\Articles2Magazine\Downloads"
    os.makedirs(downloads, exist_ok=True)
    chrome_options.add_experimental_option('prefs', {'download.default_directory': f'{downloads}'})

    # Start driver
    driver = webdriver.Chrome(executable_path="chromedriver.exe", options=chrome_options)

    # Login to website
    login = 'https://www.tourenfahrer.de/login/?tx_xtcconnect_login%5BredirectUrl%5D=https%3A%2F%2Fwww.tourenfahrer.de%2F'
    driver.get(login)
    email_field = driver.find_element(By.ID, 'login-username')
    email_field.send_keys(email)  # input('E-Mail: ')
    pw_field = driver.find_element(By.ID, 'login-password')
    pw_field.send_keys(password)  # input('Password: ')
    pw_field.submit()

    # For all years from archive
    url = 'https://www.tourenfahrer.de/motorradnews/archiv/motorradfahrer-archiv/archiv'
    driver.get(url)
    html = driver.page_source
    years = re.findall(r'motorradnews/archiv/motorradfahrer-archiv/archiv/jahr/(\S+)/\"', html)
    years = sorted(list(set(years)))
    # For all issues from a year
    for year in years:
        print(f"Getting all issues from year {year}...")
        url = f'https://www.tourenfahrer.de/motorradnews/archiv/motorradfahrer-archiv/archiv/jahr/{year}'
        driver.get(url)
        html = driver.page_source
        issues = re.findall(fr'/motorradnews/archiv/motorradfahrer-archiv/archiv/ausgabe/{year}/(\S+)/\"', html)
        issues = sorted(list(set(issues)))
        # For all parts from an issue
        for issue in issues:
            print(f"Getting all parts from issue {issue} and downloading...")
            url = f'https://www.tourenfahrer.de/motorradnews/archiv/motorradfahrer-archiv/archiv/ausgabe/{year}/{issue}/'
            driver.get(url)
            html = driver.page_source
            parts = re.findall(fr'/motorradnews/archiv/motorradfahrer-archiv/archiv/artikel/(\S+)\"', str(html))
            parts = sorted(list(set(parts)))
            for part in tqdm(parts, file=sys.stdout):
                year = part.split('/')[0]
                issue = part.split('/')[1]
                os.makedirs(f'{year}/{issue}', exist_ok=True)
                name = part.split('/')[2:-1][0]
                url = f'https://www.tourenfahrer.de/motorradnews/archiv/motorradfahrer-archiv/archiv/download///{name}'
                driver.get(url)
            for file in os.listdir('./Downloads'):
                shutil.move(f'./Downloads/{file}', f'{year}/{issue}/{file}')

    return "All done!"


if __name__ == '__main__':
    print(main())

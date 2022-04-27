import os
import re
import shutil
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from tqdm import tqdm
from config import login_config


email = login_config['email']
password = login_config['password']


def main():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-gpu')

    downloads = r"D:\Programming\Articles2Magazine\Downloads"
    os.makedirs(downloads, exist_ok=True)
    chrome_options.add_experimental_option('prefs', {'download.default_directory': f'{downloads}'})

    driver = webdriver.Chrome(executable_path=r"./chromedriver.exe", options=chrome_options)

    login = 'https://www.tourenfahrer.de/login/?tx_xtcconnect_login%5BredirectUrl%5D=https%3A%2F%2Fwww.tourenfahrer.de%2F'
    driver.get(login)
    email = driver.find_element(By.ID, 'login-username')
    email.send_keys(email)  # input('E-Mail: ')
    password = driver.find_element(By.ID, 'login-password')
    password.send_keys(password)  # input('Password: ')
    password.submit()

    url = 'https://www.tourenfahrer.de/motorradnews/archiv/motorradfahrer-archiv/archiv/ausgabe/2020/1/'
    driver.get(url)
    html = driver.page_source
    pre_link = '/motorradnews/archiv/motorradfahrer-archiv/archiv/artikel/'
    links = set(re.findall(fr'{pre_link}(\S+)\"', str(html)))
    # session.cookies.update(cookies)
    for link in tqdm(links, file=sys.stdout):
        year = link.split('/')[0]
        issue = link.split('/')[1]
        os.makedirs(f'{year}/{issue}', exist_ok=True)
        name = link.split('/')[2:-1][0]
        url = f'https://www.tourenfahrer.de/motorradnews/archiv/motorradfahrer-archiv/archiv/download///{name}'
        driver.get(url)
    for file in os.listdir('./Downloads'):
        shutil.move(f'./Downloads/{file}', f'{year}/{issue}/{file}')


if __name__ == '__main__':
    print(main())

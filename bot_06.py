import urllib
import urllib.request
import pyautogui as p
import rpa as r
import pyscreeze as py
import pandas as pd
import os
from pathlib import Path


def main():
    url = 'https://rpachallengeocr.azurewebsites.net/'
    accessible_url = connection_url_verify(url)

    site_init(url) if accessible_url else print("Bye.")

    max_window_img = img_path('max_window.png')
    move_to_center_img_click(str(max_window_img))

    p.sleep(1)
    p.hotkey('tab')
    p.press('right', presses=10)

    p.sleep(0.5)
    next_btn_img = img_path('next.png')
    extract_table_from_page(str(next_btn_img))

    r.close()


def connection_url_verify(url_to_be_verify):
    try:
        url = urllib.request.urlopen(url_to_be_verify)
    except (urllib.error.URLError):
        print("The url is not accessible. Try again.")
        return False
    else:
        print(f"The url is accessible. Code {url.getcode()}. ")
        return True


def site_init(url):
    r.init()
    r.wait(2.0)
    r.url(webpage_url=url)


def img_path(img_name):
    file_path = Path('bot_udemy_git/pv/images') # path to /images 
    return file_path / img_name


def extract_table_from_page(next_image):
    for count in range(1, 4):
        if count == 1:
            r.table('//*[@id="tableSandbox"]', 'temp.csv')
            extrc_table = pd.read_csv('temp.csv')
            extrc_table.to_csv(r'webtable.csv', mode='a', index=None, header=True)
            move_to_center_img_click(next_image, 0.7)

        else:
            r.table('//*[@id="tableSandbox"]/tbody', 'temp.csv')
            extrc_table = pd.read_csv('temp.csv')
            extrc_table.to_csv(r'webtable.csv', mode='a', index=None, header=True)
            move_to_center_img_click(next_image, 0.7)
        # os.remove('Temp.csv')


def move_to_center_img_click(img, conf=0.5):
    cordinate = center_image(img, conf)
    p.moveTo(cordinate, duration=0.4)
    p.sleep(2)
    p.click()


def center_image(img, conf):
    center_img = py.locateCenterOnScreen(img, confidence=conf)
    return center_img


if __name__ == "__main__":
    main()
import urllib
import urllib.request
import pyautogui as p
import rpa as r
import pyscreeze as py
import pandas as pd
import os


def main():
    url = 'https://rpachallengeocr.azurewebsites.net/'
    accessible_url = conection_url_verify(url)

    if accessible_url:
        site_init(url)
    else:
        print("Bye")

    image =  'max_window.png'
    move_to_center_image_click(image)

    p.sleep(1)
    p.hotkey('tab')
    p.press('right', presses=10)

    p.sleep(1.5)
    next_image = 'next.png'
    extract_table(next_image)

def conection_url_verify(url_to_be_verify):
    try:
        url = urllib.request.urlopen(url_to_be_verify)
    except (urllib.error.URLError):
        print("The url is not accessible. Try again.")
        return False
    else:
        print(f"The url is accessible. Code {url.getcode()} ")
        return True



def site_init(url):
    r.init()
    r.wait(2.0)
    r.url(webpage_url=url)




def extract_table(next_image):
    for count in range(1, 4):
        if count == 1:
            r.table('//*[@id="tableSandbox"]', 'Temp.csv')
            tabela = pd.read_csv('Temp.csv')
            tabela.to_csv(r'WebTable.csv', mode='a', index=None, header=True)
            move_to_center_image_click(next_image, 0.7)

        else:
            r.table('//*[@id="tableSandbox"]/tbody', 'Temp.csv')
            tabela = pd.read_csv('Temp.csv')
            tabela.to_csv(r'WebTable.csv', mode='a', index=None, header=True)
            move_to_center_image_click(next_image, 0.7)
        # os.remove('Temp.csv')


def move_to_center_image_click(image, conf=0.5):
    cordinate = center_image(image, conf)
    print(cordinate)
    p.moveTo(cordinate, duration=1)
    p.sleep(2)
    p.click()


def center_image(image, conf):
    center_img = py.locateCenterOnScreen(image, confidence=conf)
    return center_img


if __name__ == "__main__":
    main()
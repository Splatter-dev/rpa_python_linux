import urllib
import urllib.request
import pyautogui as p
import rpa as r
import pyscreeze as py
import pandas as pd
import os


def main():
    site = 'https://rpachallengeocr.azurewebsites.net/'
    site_acessivel = verifca_site(site)

    if site_acessivel:
        site_init(site)
    else:
        print("Tchau")

    image = 'max_window.png'
    move_to_center_image_click(image)

    p.sleep(1)
    p.hotkey('tab')
    p.press('right', presses=10)

    p.sleep(1.5)
    next_image = 'next.png'
    extract_table(next_image)


def site_init(url):
    r.init()
    r.wait(2.0)
    r.url(webpage_url=url)


def verifca_site(site_a_ser_verificado):
    try:
        url = urllib.request.urlopen(site_a_ser_verificado)
    except (urllib.error.URLError):
        print("o Site não está acessivel.")
        return False
    else:
        print(f"Tudo ok. Codigo {url.getcode()} ")
        return True


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
        os.remove('Temp.csv')


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
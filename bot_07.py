import urllib
import urllib.request
import pandas as pd
import rpa as r


def main():
    url = 'http://rpachallenge.com'
    accessible_url = connection_url_verify(url)

    if accessible_url:
        web_page_init(url)
    else:
        print("Bye.")

    r.wait(2)

    workbook = download_workbook(file_name='workbook.xlsx')
    op_workbook = open_workbook(workbook)

    data_frame = workbook_df(op_workbook)
    labels_list = lb_list()

    start_challenge(data_frame, labels_list)
    end_challenge()


def connection_url_verify(url_to_be_verify):
    try:
        url = urllib.request.urlopen(url_to_be_verify)
    except (urllib.error.URLError):
        print("The url is not accessible. Try again.")
        return False
    else:
        print(f"The url is accessible. Code {url.getcode()}. ")
        return True


def web_page_init(url):
    r.init()
    r.wait(2.0)
    r.url(webpage_url=url)


def download_workbook(file_name):
    r.download('http://rpachallenge.com/assets/downloadFiles/challenge.xlsx',f'{file_name}')
    return file_name


def open_workbook(workbook):
    opened_file = pd.read_excel(f'{workbook}',sheet_name='Sheet1',engine='openpyxl')
    return opened_file


def workbook_df(workbook):
    data_frame = pd.DataFrame(workbook,
                              columns=[
                                  'First Name', 'Last Name ', 'Company Name',
                                  'Role in Company', 'Address', 'Email',
                                  'Phone Number'
                              ])
    return data_frame


def lb_list():
    labels = [
        "labelFirstName", "labelLastName", "labelCompanyName", "labelRole",
        "labelAddress", "labelEmail", "labelPhone"
    ]
    return labels


def start_challenge(data_frame, labels_list):
    r.click('/html/body/app-root/div[2]/app-rpa1/div/div[1]/div[6]/button')
    count_round = 1

    for row in data_frame.itertuples():
        if count_round == 11:
            break
        
        else:
            for label in range(0, 7):
                row_converted_to_string = str(row[label + 1])
                if label == 6:
                    r.type(f'//*[@ng-reflect-name="{labels_list[label]}"]', row_converted_to_string[:-2])
                else:
                    r.type(f'//*[@ng-reflect-name="{labels_list[label]}"]', row_converted_to_string)

            r.click('/html/body/app-root/div[2]/app-rpa1/div/div[2]/form/input')
            count_round += 1


def end_challenge():
    r.snap('page', 'registry.png')
    r.wait(1)
    r.close()


if __name__ == "__main__":
    main()
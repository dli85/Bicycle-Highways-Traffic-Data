from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os.path
import glob
from pathlib import Path
import natsort
import shutil

from csvReader import read_csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = 'https://scerisecm.boston.gov/ScerIS/CmPublic/#/SearchCriteria?f=56'
csv_path = 'search results.csv'
project_path = 'C:\\Users\\dali7\\PycharmProjects\\Traffic-data-scraper'
temp_directory_path = project_path + '\\temp'
download_directory_path = project_path + '\\downloads'

temp_directory_path_relative = './temp'
download_directory_path_relative = './downloads'

file_id = 1

currentRow = 0
search_list = []


def create_list(starting):
    global search_list
    search_list = read_csv(csv_path, starting)


def crawl():
    global search_list
    global currentRow
    global file_id

    # Change download directory to a local folder
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': temp_directory_path}
    chrome_options.add_experimental_option('prefs', prefs)

    driver = webdriver.Chrome('./driver/chromedriver.exe', options=chrome_options)
    driver.get(url)

    # Select archive date
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//body[@id='dmsBody']/div[@ng-hide='unload']/div["
                                              "@class='ng-scope']/div[@class='ng-scope']/div["
                                              "@class='container']/div[@id='view']/div["
                                              "@class='ng-scope']/form[@class='sc-form-page paddingLeft15 "
                                              "ng-pristine ng-valid ng-scope ng-isolate-scope "
                                              "ng-valid-range ng-valid-date ng-valid-sceris-date "
                                              "ng-valid-pattern']/div["
                                              "@class='sc-form-page-form-outer']/div["
                                              "@class='sc-form-page-form-inner']/div[@class='row "
                                              "searchPageContainer ng-scope']/div[@class='col-md-12 "
                                              "searchPaneZindex ng-scope']/loading-spinner["
                                              "@class='ng-isolate-scope']/span["
                                              "@data-ng-hide='showSpinner']/div["
                                              "@class='ng-scope']/div/div[@class='row']/div["
                                              "@class='col-md-12']/loading-spinner[@class='ng-scope "
                                              "ng-isolate-scope']/span[@data-ng-hide='showSpinner']/div["
                                              "@class='mayDrag ng-pristine ng-untouched ng-valid ng-scope "
                                              "ng-isolate-scope ui-sortable ui-sortable-disabled']/div["
                                              "1]/span[2]/span[1]/div[1]/div[1]/criterion-operation["
                                              "1]/li[1]/a[1]"))).click()
    # archive_date_selector.click()
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//li[@class='dropdown sc-input-narrow-width cursor-default "
                                              "open']//ul[@class='dropdown-menu available-items']//li["
                                              "@class='criterion-operation-list-item'][contains(text(),"
                                              "'Not Blank')]"))).click()

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[1]/div["
                                                                          "2]/div[3]/div[2]/form[ "
                                                                          "1]/div[2]/div[1]/div[2]/"
                                                                          "div[1]/button[1]"))).click()

    time.sleep(3)
    try:
        for i in range(currentRow, len(search_list)):
            print("Progress: working on", str(currentRow + 1), "/", str(len(search_list)))

            string = search_list[i]
            # original_file field
            original_file_field = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div[3]/div/div/div["
                                                                "2]/div[ "
                                                                "1]/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/div["
                                                                "1]/div[ "
                                                                "1]/div/div/div/div/div/div[7]/div[2]/div["
                                                                "2]/div/div/input")
            original_file_field.clear()
            original_file_field.send_keys(string)

            # click archive_date_sort twice
            WebDriverWait(driver, 10) \
                .until(EC.element_to_be_clickable((By.XPATH,
                                                   "/html/body/div[1]/div/div/div[2]/div[3]/div/div/div[2]/div["
                                                   "1]/div[2]/div[2]/div[2]/div/div[2]/div["
                                                   "2]/div/div[1]/div[ "
                                                   "1]/div/div/div/div/div/div[1]/div[1]/div[1]"))).click()
            WebDriverWait(driver, 10) \
                .until(EC.element_to_be_clickable((By.XPATH,
                                                   "/html/body/div[1]/div/div/div[2]/div[3]/div/div/div[2]/div["
                                                   "1]/div[2]/div[2]/div[2]/div/div[2]/div["
                                                   "2]/div/div[1]/div[ "
                                                   "1]/div/div/div/div/div/div[1]/div[1]/div[1]"))).click()

            study_type = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div[3]/div/div/div[2]/div["
                                                       "1]/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/div[1]/div["
                                                       "2]/div/div[1]/div/div[11]/div").text

            # select row and click

            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,
                                                                        "/html/body/div[1]/div/div/div["
                                                                        "2]/div[3]/div/div/div[2]/div["
                                                                        "1]/div[2]/div[ "
                                                                        "2]/div[2]/div/div[2]/div[2]/div/div[1]/div["
                                                                        "2]/div/div/div/div[1]/div"))).click()

            # Select and click view document button
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div["
                                                                                  "2]/div[3]/div/div/div[2]/div["
                                                                                  "1]/div[2]/div[ "
                                                                                  "2]/div[2]/div/div[1]/nav/button[5]"))
                                            ).click()
            # select and click download
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div["
                                                                                  "2]/div[3]/div/div[3]/div[1]/div["
                                                                                  "2]/div/div[ "
                                                                                  "4]/div[2]/div[1]/div[2]/div["
                                                                                  "1]/button[3]"))).click()
            time.sleep(1)
            # select and hit download left side
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div["
                                                                                  "2]/div[3]/div/div[3]/div[1]/div["
                                                                                  "2]/div/div[ "
                                                                                  "4]/div[5]/div["
                                                                                  "7]/div[2]/button"))).click()

            # select and hit save
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[1]/div/div/div[2]/div[3]/div/div[3]/div[1]/div[2]/div/div["
                           "4]/div[23]/div/div/div[2]/button[2]"))).click()
            time.sleep(1)
            for x in os.walk(temp_directory_path):
                download_file_path = x[0] + '\\' + x[2][0]
                filetype = x[2][0].split('.')[len(x[2][0].split('.')) - 1]
                # print(download_file_path + " " + filetype)

                new_path = download_directory_path + '\\' + "Type " + study_type + " " + str(file_id) + \
                           "." + filetype
                # print(new_path)
                Path(download_directory_path).mkdir(parents=True, exist_ok=True)
                time.sleep(0.2)
                shutil.copy2(download_file_path, new_path)
                time.sleep(0.2)
                os.remove(download_file_path)
                os.rmdir(temp_directory_path)
                break

            time.sleep(1)

            # files = glob.iglob('.\\downloads\\*')
            # max_file = max(files, key=os.path.getctime)
            # original_file_name = max_file
            # max_file_split = max_file.split('\\')
            # filename = max_file_split[len(max_file_split) - 1].split('.')
            # extension = filename[len(filename) - 1]
            # # print(max_file_split)
            # # print(filename)
            # # print(extension)
            # new_file_name = "Type " + study_type + " " + str(currentRow) + "." + extension
            # # print(new_file_name)
            # os.rename(original_file_name, '.\\downloads\\' + new_file_name)

            # hit back button
            driver.find_element(By.XPATH, '//*[@id="btnBackToSearchResult"]').click()
            currentRow += 1
            file_id += 1

            time.sleep(0.5)
    except ValueError:
        driver.close()
        print("restarting... (nothing to worry about)")
        time.sleep(10)
        crawl()
        return

    driver.close()


if __name__ == '__main__':
    change_starting_point = input("Change starting point of the csv[y/n]? ")

    starting_point = 0

    if change_starting_point.lower() == 'y':
        start = int(input("What line of the csv do you want to start at (use 0 indexing)? "))
        starting_point = start

    create_list(starting_point)
    crawl()

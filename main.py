from selenium import webdriver

url = 'https://scerisecm.boston.gov/ScerIS/CmPublic/#/Results'


if __name__ == '__main__':
    driver = webdriver.Chrome('./driver/chromedriver.exe')
    driver.get(url)

    # driver.close()

    print("done")

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_driver_path = r'C:\Users\luana\Desktop\chromedriver-win64\chromedriver.exe'

service = Service(chrome_driver_path)
service.start()
options = webdriver.ChromeOptions()
options.add_argument('--headless') 
driver = webdriver.Chrome(service=service, options=options)

try:
    url = 'https://www.twitch.tv/directory/all/tags/kids'
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[data-focusable="true"][data-test-selector="TitleAndChannel"][data-a-target="preview-card-channel-link"]')))
    for element in elements:
        print(element.get_attribute('href'))

finally:
    driver.quit()

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['mails']
mails = db.mails

hrefs = []
header = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0'}
username = 'study.ai_172@mail.ru'
password = 'NextPassword172???'
site = 'e.mail.ru/'
chrome_options = Options()
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)
driver.get('https://mail.ru/')
elem = driver.find_element_by_xpath("//input[@name='login']")
elem.send_keys(username)

button = driver.find_element_by_xpath("//button[@data-testid='enter-password']")
button.click()
wait = WebDriverWait(driver, 10)
elem = wait.until(ec.visibility_of_element_located((By.XPATH, "//input[@type='password']")))
elem.send_keys(password)

button = wait.until(ec.element_to_be_clickable((By.XPATH, "//button[@data-testid='login-to-mail']")))
button.click()

time.sleep(10)
href = driver.find_elements_by_xpath("//a[contains(@class, 'js-letter-list-item')]")
a = 0
b = 1
while True:
    a = href[-1]
    actions = ActionChains(driver)
    actions.move_to_element(href[-1])
    hrefs.append(href[-3])
    time.sleep(3)
    actions.perform()
    href = driver.find_elements_by_xpath("//a[contains(@class, 'js-letter-list-item')]")
    b = href[-1]
    if a == b:
        break
emails = []
for i in hrefs:
    email = {}
    href = i.get_attribute('href')
    driver.get(href)
    try:
        button_wait = wait.until(ec.presence_of_element_located((By.CLASS_NAME, 'letter__date')))
        email['date'] = driver.find_element_by_class_name('letter__date').text
        email['name'] = driver.find_element_by_class_name('letter-contact').text
        email['name_email'] = driver.find_element_by_class_name('letter-contact').get_attribute('title')
        email['topic'] = driver.find_element_by_class_name('letter__body').text
        emails.append(email)
        mails.insert_one(email)
    except:
        continue
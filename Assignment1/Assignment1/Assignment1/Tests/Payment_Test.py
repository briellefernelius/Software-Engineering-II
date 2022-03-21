from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

# call the driver to run the web browser
service = Service(executable_path=ChromeDriverManager().install())
options = Options()
options.page_load_strategy = 'normal'

driver = webdriver.Chrome(service=service, options=options)
driver.set_window_size(1920, 1080)

# Go to website
driver.get("http://127.0.0.1:8000/")
time.sleep(1.73)

# Go to the username element and enter the string
driver.find_element(By.NAME, "username").send_keys("ryan@mail.com")
time.sleep(0.5)

driver.find_element(By.NAME, "password").send_keys("Boring1234")
time.sleep(0.5)

# find the sign in button and then click it
# go to homepage...
driver.find_element(By.NAME, "Signin_Button").click()
time.sleep(0.75)

# go to account page
driver.find_element(By.NAME, "Account_Button").click()
time.sleep(0.5)

# enter cardholder name
driver.find_element(By.NAME, "cardholder_name").send_keys("Ryan Ashley")
time.sleep(0.3)

# enter card number
driver.find_element(By.NAME, "card_number").send_keys("4242424242424242")
time.sleep(0.75)

# click expiration month
# 1 - turn the find statement into a Select object
# 2 - then select by value and get the value of november (11)
select = Select(driver.find_element(By.NAME, "expiration_month"))
driver.find_element(By.NAME, "expiration_month").click()
time.sleep(0.3)
select.select_by_value('11')
time.sleep(0.75)

# click expiration year
select = Select(driver.find_element(By.NAME, "expiration_year"))
driver.find_element(By.NAME, "expiration_year").click()
time.sleep(0.3)
select.select_by_value('2026')
time.sleep(0.75)

# enter cvc number
driver.find_element(By.NAME, "cvc_number").send_keys("123")
time.sleep(0.75)

# enter amount
driver.find_element(By.NAME, "amount").send_keys("200")
time.sleep(0.75)

# click pay tuition button
driver.find_element(By.NAME, "Pay_Button").click()
time.sleep(3)


driver.quit()

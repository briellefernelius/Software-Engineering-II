from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
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
time.sleep(1)

driver.find_element(By.NAME, "password").send_keys("Boring1234")
time.sleep(1)

# find the sign in button and then click it
# go to homepage...
driver.find_element(By.NAME, "Signin_Button").click()
time.sleep(3)


driver.find_element(By.NAME, "Logout_Button").click()
time.sleep(1)

driver.find_element(By.NAME, "Logout_Button").click()
time.sleep(3)

driver.quit()


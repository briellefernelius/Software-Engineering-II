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
driver.find_element(By.NAME, "username").send_keys("mike@gmail.com")
time.sleep(0.5)

driver.find_element(By.NAME, "password").send_keys("welove1234")
time.sleep(0.5)

# find the sign in button and then click it
# go to homepage...
driver.find_element(By.NAME, "Signin_Button").click()
time.sleep(0.75)

# go to register page
driver.find_element(By.NAME, "Register_Button").click()
time.sleep(0.5)

# click to register for a class
driver.find_element(By.NAME, "RegisterClass_Button").click()
time.sleep(3)

# go back to dashboard to see class was registered for
driver.find_element(By.NAME, "Dashboard_Button").click()
time.sleep(3)

# go back to register page
driver.find_element(By.NAME, "Register_Button").click()
time.sleep(0.5)

# click to drop a course
driver.find_element(By.NAME, "Drop_Button").click()
time.sleep(1)

# go back to dashboard to show course was dropped
driver.find_element(By.NAME, "Dashboard_Button").click()
time.sleep(3)

driver.quit()

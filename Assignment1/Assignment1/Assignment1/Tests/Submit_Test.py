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
driver.find_element(By.NAME, "username").send_keys("student1@gmail.com")
time.sleep(0.5)

driver.find_element(By.NAME, "password").send_keys("stayout1234")
time.sleep(0.5)

# find the sign in button and then click it
# go to homepage...
driver.find_element(By.NAME, "Signin_Button").click()
time.sleep(0.75)

#Go to course
driver.find_element(By.NAME, "view_course").click()
time.sleep(0.5)

#Go to assignment
driver.find_element(By.NAME, "view_assignment").click()
time.sleep(0.5)

#Add text and submit assignment
driver.find_element(By.NAME, "textbox").send_keys("Test Submission")
time.sleep(2)

#Submit
driver.find_element(By.NAME, "submit_assignment").click()
time.sleep(1)

#Go to assignment see its submitted
driver.find_element(By.NAME, "view_assignment").click()
time.sleep(3)

driver.quit()

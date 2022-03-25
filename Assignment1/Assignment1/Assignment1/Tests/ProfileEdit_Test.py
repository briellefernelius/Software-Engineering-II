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

# go to profile page
driver.find_element(By.NAME, "_Button").click()
time.sleep(0.5)

# backup dict to store origional information: this is for reverting changes
bak_d = {}

# click to edit button for a class
driver.find_element(By.NAME, "editButton").click()
time.sleep(1.5)

# backup the first name, and change it
fname = driver.find_element(By.ID, 'id_first_name')
bak_d['firstname'] = fname.get_attribute('value')
fname.clear()
fname.send_keys('test first name')  # takes value sends it to element
time.sleep(1.5)
# backup the last name, and change it (bak_d = backup dictionary)
lname = driver.find_element(By.ID, 'id_last_name')
bak_d['lastname'] = lname.get_attribute('value')
lname.clear()  # clear the field of values before we send anything into it
lname.send_keys('test last name')  # send values to the target field
time.sleep(1.5)
# save the changes (svbtn save button)
svbtn = driver.find_element(By.NAME, 'saveProfileChanges')
driver.execute_script("arguments[0].click()", svbtn)  # Click the save button
time.sleep(3)

# begin the process of reverting changes
driver.find_element(By.NAME, "editButton").click()
time.sleep(1.5)
# Sets first name equal to backup
fname = driver.find_element(By.ID, 'id_first_name')
fname.clear()
fname.send_keys(bak_d['firstname'])
time.sleep(1.5)
# Sets last name equal to backup
lname = driver.find_element(By.ID, 'id_last_name')
lname.clear()  # clear the field of values before we send anything into it
lname.send_keys(bak_d['lastname'])  # send values to the target field
time.sleep(1.5)
svbtn = driver.find_element(By.NAME, 'saveProfileChanges')
driver.execute_script("arguments[0].click()", svbtn)
time.sleep(3)

# fname.clear()
# fname.send_keys(bak_d['firstname'])
# time.sleep(3)
# lname.clear()
# lname.send_keys(bak_d['lastname'])
# time.sleep(3)

# driver.find_element(By.NAME, "Dashboard_Button").click()
# time.sleep(3)

driver.quit()

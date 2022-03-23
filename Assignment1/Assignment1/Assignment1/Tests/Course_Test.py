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
driver.find_element(By.NAME, "username").send_keys("tim@gmail.com")
time.sleep(0.5)

driver.find_element(By.NAME, "password").send_keys("Boring1234")
time.sleep(0.5)

# find the sign in button and then click it
# go to homepage...
driver.find_element(By.NAME, "Signin_Button").click()
time.sleep(0.75)

# go to register page
driver.find_element(By.NAME, "Courses_Button").click()
time.sleep(2)

# click to register for a class
driver.find_element(By.NAME, "add_course_button").click()
time.sleep(2)

# enter course name
driver.find_element(By.NAME, "course_number").send_keys("CS 3030")
time.sleep(0.3)

# enter course name
driver.find_element(By.NAME, "course_name").send_keys("Scripting Languages")
time.sleep(0.75)

# enter credit hours
driver.find_element(By.NAME, "credit_hours").send_keys("4")
time.sleep(0.75)

# select meeting days
driver.find_element(By.NAME, "meeting_time_days").send_keys('Monday')
driver.find_element(By.NAME, "meeting_time_days").click()
time.sleep(0.3)

# enter start time
driver.find_element(By.NAME, "start_time").send_keys("9:00 AM")
time.sleep(0.75)

# enter end time
driver.find_element(By.NAME, "end_time").send_keys("10:30 AM")
time.sleep(0.75)

# enter start date
driver.find_element(By.NAME, "start_date").send_keys("1/16/2022")
time.sleep(0.75)

# enter end date
driver.find_element(By.NAME, "end_date").send_keys("4/28/2022")
time.sleep(0.75)

driver.find_element(By.NAME, "SaveCourse_Button").click()
time.sleep(0.5)

driver.find_element(By.NAME, "Courses_Button").click()
time.sleep(2)

driver.find_element(By.NAME, "DeleteCourse_Button").click()
time.sleep(2)

driver.find_element(By.NAME, "ConfirmDelete_Button").click()
time.sleep(2)

driver.find_element(By.NAME, "Courses_Button").click()
time.sleep(1)

driver.quit()


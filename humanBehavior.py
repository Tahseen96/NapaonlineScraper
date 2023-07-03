import random
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC


# function to wait for an element to be appeared
def waitForElement(driver_arg, xpath, wait=10):
    WebDriverWait(driver_arg, wait).until(
        EC.presence_of_element_located((By.XPATH, xpath)))
    
# function to click on an element if it's clickable
def humanClick(driver_arg, xpath, wait=10):
    element = WebDriverWait(driver_arg, wait).until(
        EC.element_to_be_clickable((By.XPATH, xpath)))
    element.click()
    
# function to get an element
def getElement(driver_arg,xpath,wait=10):
    element = WebDriverWait(driver_arg, wait).until(
        EC.presence_of_element_located((By.XPATH, xpath)))
    return element

# function to type anything in the input field
def humanTyper(driver_arg, xpath, text, wait=10):
    element = WebDriverWait(driver_arg, wait).until(
        EC.presence_of_element_located((By.XPATH, xpath)))
    for character in text:
        element.send_keys(character)
        sleep(random.uniform(0.01, 0.02))
        
# function to select an option from the dropdown
def selectOption(driver_arg,xpath,option):
    select = Select(getElement(driver_arg,xpath))
    select.select_by_value(option)

# function to clear any input field by the element id
def clearSearchField(driver_arg,element_id):
    driver_arg.execute_script("""
    let element = document.getElementById('{}')
    element.value = ''
    """.format(element_id))
    
# function for random wait between to given intergers
def randomWait(lower_limit, uper_limit):
    time_wait = random.randint(lower_limit, uper_limit)
    sleep(time_wait)

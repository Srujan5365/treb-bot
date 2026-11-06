import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from screens.trebb_allfunctions import get_traceback,check_exceptiondict

def login_page(driver,trebbUrl,trebbUsername,trebbPassword,exceptionDict,logger):
    try:
        time.sleep(2)
        driver.get(trebbUrl)
        logger.info("Trebb URL Launched Successfully")
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "username")))
        except TimeoutException:
            pass
        driver.find_element(By.ID,"username").clear()
        driver.find_element(By.ID,"username").send_keys(trebbUsername)
        time.sleep(0.5)
        logger.info("Trebb Username is Entered")
        driver.find_element(By.ID,"password").clear()
        driver.find_element(By.ID,"password").send_keys(trebbPassword)
        time.sleep(0.5)
        logger.info("Trebb Password is Entered")
        submitButton=driver.find_element(By.XPATH,"//input[@name='login' and @type='submit' and @value='Submit']")
        driver.execute_script("arguments[0].click();", submitButton)
        time.sleep(2)
        logger.info("Submit Button is Clicked")

    except Exception as e:
        logger.error(e)
        if check_exceptiondict(exceptionDict):
            exceptionDict["Status"]="Failed"
            exceptionDict["Exception type"]="Application"
            exceptionDict["Exception Message"]=get_traceback(e)
        raise

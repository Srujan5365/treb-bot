import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from selenium.webdriver.common.keys import Keys
from screens.trebb_allfunctions import get_traceback, check_exceptiondict,fill_dropdown,fill_textbox,fill_yesnobutton,fill_combobox,check_ui_errors


def draft_photos_page(driver, Listings_Dict, exceptionDict, logger):
    try:
        if Listings_Dict.get("DraftPhotos_PhotoPaths",""):
            file_input = driver.find_element(By.XPATH, "//input[@type='file']")
            photoPaths=Listings_Dict["DraftPhotos_PhotoPaths"].split("$")
            numberOfPhotos=len(photoPaths)
            file_input.send_keys("\n".join(photoPaths))
            time.sleep(3)

            for i in range(1,numberOfPhotos+1):
                fill_textbox(driver,f'(//textarea[@id="shortDescription"])[{i}]',Listings_Dict,f"DraftPhotos_Description_{i}",exceptionDict,logger,useXpath=True)

            validateButton = driver.find_element(By.XPATH,'//button[.//mat-icon[normalize-space(.)="rule"] and .//span[contains(normalize-space(.),"Validate")]]')
            driver.execute_script("arguments[0].click();", validateButton)
            time.sleep(3)
        
        check_ui_errors(driver)
        nextButton = driver.find_element(By.XPATH,'//button[.//span[contains(@class,"mdc-button__label") and normalize-space()="Next"]]')
        driver.execute_script("arguments[0].click();", nextButton)
        time.sleep(5)
    except Exception as e:
        logger.error(e)
        if check_exceptiondict(exceptionDict):
            exceptionDict["Status"] = "Failed"
            exceptionDict["Exception type"] = "Application"
            exceptionDict["Exception Message"] = get_traceback(e)
        raise


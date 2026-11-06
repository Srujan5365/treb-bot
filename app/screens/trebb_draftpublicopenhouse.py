import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from selenium.webdriver.common.keys import Keys
from screens.trebb_allfunctions import get_traceback, check_exceptiondict,fill_dropdown,fill_textbox,fill_yesnobutton,fill_combobox,check_ui_errors


def draft_publicopenhouse_page(driver, Listings_Dict, exceptionDict, logger):
    try:
        for roomNumber in range(1,int(Listings_Dict["DraftPublicOpenHouse_NumberOfPublicOpenHouses"])+1):
            if len(driver.find_elements(By.XPATH, '//mat-select[@id="OpenHouse[].OpenHouseStatus"]')) < roomNumber:
                addAnotherOpenHouse=driver.find_element(By.XPATH, "//button[.//span[contains(normalize-space(), 'Add another Open House')]]")
                driver.execute_script("arguments[0].click();", addAnotherOpenHouse)            
                time.sleep(2)
            
            fill_dropdown(driver,f'(//mat-select[@id="OpenHouse[].OpenHouseStatus"])[{roomNumber}]',Listings_Dict,"DraftPublicOpenHouse_OpenHouseStatus_"+str(roomNumber),exceptionDict,logger,useXpath=True)

            fill_dropdown(driver,f'(//mat-select[@id="OpenHouse[].OpenHouseType"])[{roomNumber}]',Listings_Dict,"DraftPublicOpenHouse_OpenHouseType_"+str(roomNumber),exceptionDict,logger,useXpath=True)

            fill_dropdown(driver,f'(//mat-select[@id="OpenHouse[].OpenHouseFormat"])[{roomNumber}]',Listings_Dict,"DraftPublicOpenHouse_OpenHouseFormat_"+str(roomNumber),exceptionDict,logger,useXpath=True)
            
            fill_textbox(driver,f'(//input[@id="OpenHouse[].OpenHouseDate"])[{roomNumber}]',Listings_Dict,"DraftPublicOpenHouse_OpenHouseDate_"+str(roomNumber),exceptionDict,logger,useXpath=True)
            time.sleep(1)
            # Start Time
            startTimeButton = driver.find_element(By.XPATH, f"(//mat-label[normalize-space()='Start Time']/ancestor::mat-form-field//input[@role='combobox'])[{roomNumber}]")
            driver.execute_script("arguments[0].click();", startTimeButton)
            time.sleep(1)
            startTimeFieldButton = driver.find_element(By.XPATH, f"//mat-option[@role='option'][.//span[normalize-space()='{Listings_Dict['DraftPublicOpenHouse_StartTime_'+str(roomNumber)].strip()}']]")
            driver.execute_script("arguments[0].click();", startTimeFieldButton)
            time.sleep(1)

            # End Time
            endTimeButton = driver.find_element(By.XPATH, f"(//mat-label[normalize-space()='End Time']/ancestor::mat-form-field//input[@role='combobox'])[{roomNumber}]")
            driver.execute_script("arguments[0].click();", endTimeButton)
            time.sleep(1)
            endTimeFieldButton = driver.find_element(By.XPATH, f"//mat-option[@role='option'][.//span[normalize-space()='{Listings_Dict['DraftPublicOpenHouse_EndTime_'+str(roomNumber)].strip()}']]")
            driver.execute_script("arguments[0].click();", endTimeFieldButton)
            time.sleep(1)

            fill_textbox(driver,f'(//input[@id="OpenHouse[].OpenHouseRemarks"])[{roomNumber}]',Listings_Dict,"DraftPublicOpenHouse_OpenHouseNotes_"+str(roomNumber),exceptionDict,logger,useXpath=True)

            
        time.sleep(3)
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
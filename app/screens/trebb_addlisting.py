import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from screens.trebb_allfunctions import get_traceback, check_exceptiondict,fill_textbox,fill_dropdown,fill_combobox,fill_yesnobutton

# Angular Material renders every opened dropdown panel inside a cdk-overlay-pane.
# Auto-generated ids (mat-select-141, mat-input-313, mat-option-2651 ...) change on every
# page load, so they are NOT used anywhere below. We rely on:
#   - fixed ids        : ListOfficeKey, StreetNumber, PostalCode ...
#   - aria-label       : Search By, Owner Name, Search by Address ...
#   - visible option text inside the overlay panel
OVERLAY = "//div[contains(@class,'cdk-overlay-pane')]"


def add_listing_page(driver, Listings_Dict, exceptionDict, logger):
    """Runs the complete sequence for the Add Listing screen."""
    try:
        WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, "//mat-select[@aria-label='Search By']")))

        clearButton = driver.find_element(By.XPATH, "//button[@aria-label='Clear']")
        driver.execute_script("arguments[0].click();", clearButton)
        time.sleep(2)

        #fill_dropdown(driver,"",Listings_Dict,"",exceptionDict,logger)
        #fill_textbox(driver,"",Listings_Dict,"",exceptionDict,logger)

        mode=Listings_Dict.get("AddListing_SearchBy","").lower()
        if mode:
            searchByField=driver.find_element(By.XPATH, "//mat-select[@aria-label='Search By']")
            driver.execute_script("arguments[0].click();",searchByField)
            time.sleep(2)
            searchByFieldOption = driver.find_element(By.XPATH, OVERLAY + f"//mat-option[.//span[normalize-space()='{Listings_Dict["AddListing_SearchBy"]}']]")
            driver.execute_script("arguments[0].click();", searchByFieldOption)
            time.sleep(1)
            
            if mode == "address":
                driver.find_element(By.XPATH, "//input[@aria-label='Search by Address']").clear()
                driver.find_element(By.XPATH, "//input[@aria-label='Search by Address']").send_keys(Listings_Dict["AddListing_Address"])
                time.sleep(3)
                addressElement = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//mat-option[@role='option']//div[@class='public-search-address' and contains(text(), '{Listings_Dict["AddListing_Address"]}')]")))
                driver.execute_script("arguments[0].click();", addressElement)
            elif mode == "owner":
                lroField=driver.find_element(By.XPATH, "//mat-select[@aria-label='LRO']")
                driver.execute_script("arguments[0].click();", lroField)
                time.sleep(1)
                lroFieldOption = driver.find_element(By.XPATH, OVERLAY + f"//mat-option[.//span[normalize-space()='{Listings_Dict["AddListing_LRO"]}']]")
                driver.execute_script("arguments[0].click();", lroFieldOption)
                time.sleep(1)
                driver.find_element(By.XPATH, "//input[@aria-label='Owner Name']").clear()
                driver.find_element(By.XPATH, "//input[@aria-label='Owner Name']").send_keys(Listings_Dict["AddListing_OwnerName"])
            elif mode == "pin":
                driver.find_element(By.XPATH, "//input[@aria-label='Property Identification Number']").clear()
                driver.find_element(By.XPATH, "//input[@aria-label='Property Identification Number']").send_keys(Listings_Dict["AddListing_PIN"])
            elif mode == "arn":
                driver.find_element(By.XPATH, "//input[@aria-label='Assessment Roll Number']").clear()
                driver.find_element(By.XPATH, "//input[@aria-label='Assessment Roll Number']").send_keys(Listings_Dict["AddListing_ARN"])
            time.sleep(1)

        fill_dropdown(driver,"ListAgentKey",Listings_Dict,"AddListing_Member",exceptionDict,logger,searchMode=True)

        fill_dropdown(driver,"TransactionType",Listings_Dict,"AddListing_TransactionType",exceptionDict,logger)

        fill_dropdown(driver,"PropertyType",Listings_Dict,"AddListing_PropertyClass",exceptionDict,logger)

        fill_dropdown(driver,"PropertySubType",Listings_Dict,"AddListing_PropertyType",exceptionDict,logger,searchMode=True)
        
        fill_textbox(driver,"StreetNumber",Listings_Dict,"AddListing_StreetNumber",exceptionDict,logger)

        fill_textbox(driver,"StreetName",Listings_Dict,"AddListing_StreetName",exceptionDict,logger)

        fill_dropdown(driver,"StreetSuffix",Listings_Dict,"AddListing_Abbreviation",exceptionDict,logger,searchMode=True)

        fill_dropdown(driver,"StreetDirSuffix",Listings_Dict,"AddListing_StreetDirection",exceptionDict,logger)

        fill_textbox(driver,"UnitNumber",Listings_Dict,"AddListing_UnitNumber",exceptionDict,logger)

        fill_dropdown(driver,"CountyOrParish",Listings_Dict,"AddListing_Area",exceptionDict,logger,searchMode=True)

        fill_dropdown(driver,"City",Listings_Dict,"AddListing_Municipality",exceptionDict,logger,searchMode=True)

        fill_dropdown(driver,"CityRegion",Listings_Dict,"AddListing_Community",exceptionDict,logger,searchMode=True)

        fill_textbox(driver,"PostalCode",Listings_Dict,"AddListing_PostalCode",exceptionDict,logger)

        print("")
        createButton = driver.find_element(By.XPATH, "//button[@aria-label='Create Listing']")
        driver.execute_script("arguments[0].click();", createButton)
        time.sleep(5)

    except Exception as e:
        logger.error(e)
        if check_exceptiondict(exceptionDict):
            exceptionDict["Status"] = "Failed"
            exceptionDict["Exception type"] = "Application"
            exceptionDict["Exception Message"] = get_traceback(e)
        raise
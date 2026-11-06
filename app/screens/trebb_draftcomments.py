import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from selenium.webdriver.common.keys import Keys
from screens.trebb_allfunctions import get_traceback, check_exceptiondict,fill_dropdown,fill_textbox,fill_yesnobutton,fill_combobox,check_ui_errors

OVERLAY = "//div[contains(@class,'cdk-overlay-pane')]"

#fill_dropdown(driver,"",Listings_Dict,"",exceptionDict,logger)
#fill_textbox(driver,"",Listings_Dict,"",exceptionDict,logger)
#fill_yesnobutton(driver,"","",Listings_Dict,"",exceptionDict,logger)
#fill_combobox(driver,"",Listings_Dict,"",exceptionDict,logger,searchMode=True)


def draft_comments_page(driver, Listings_Dict, exceptionDict, logger):
    try:
        
        fill_textbox(driver,"PublicRemarks",Listings_Dict,"DraftComments_RemarksForClients",exceptionDict,logger)

        fill_textbox(driver,"OfferRemarks",Listings_Dict,"DraftComments_OfferRemarks",exceptionDict,logger)

        fill_textbox(driver,"Inclusions",Listings_Dict,"DraftComments_Inclusions",exceptionDict,logger)

        fill_textbox(driver,"Exclusions",Listings_Dict,"DraftComments_Exclusions",exceptionDict,logger)

        fill_textbox(driver,"RentalItems",Listings_Dict,"DraftComments_RentalItems",exceptionDict,logger)

        fill_textbox(driver,"RentalItemsMonthlyCost",Listings_Dict,"DraftComments_UnderContractMonthlyCosts",exceptionDict,logger)

        fill_textbox(driver,"PrivateRemarks",Listings_Dict,"DraftComments_RealtorOnlyRemarks",exceptionDict,logger)

        #fill_textbox(driver,"SystemRemarks",Listings_Dict,"DraftComments_SystemRemarks",exceptionDict,logger)
        
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
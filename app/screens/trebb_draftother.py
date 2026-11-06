import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from selenium.webdriver.common.keys import Keys
from screens.trebb_allfunctions import get_traceback, check_exceptiondict,fill_dropdown,fill_textbox,fill_yesnobutton,fill_combobox,check_ui_errors


def draft_other_page(driver, Listings_Dict, exceptionDict, logger):
    try:

        fill_dropdown(driver,"ListOfficeKey",Listings_Dict,"DraftOther_ListingBrokerage",exceptionDict,logger)

        fill_textbox(driver,"ListOfficePhone",Listings_Dict,"DraftOther_ListingBrokeragePhone",exceptionDict,logger)

        fill_textbox(driver,"ListOfficeFax",Listings_Dict,"DraftOther_ListingBrokerageFax",exceptionDict,logger)

        fill_dropdown(driver,"ListAgentKey",Listings_Dict,"DraftOther_SalesPerson_1",exceptionDict,logger,searchMode=True)

        fill_textbox(driver,"ListAgentDirectPhone",Listings_Dict,"DraftOther_SalesPersonPhone_1",exceptionDict,logger)

        fill_textbox(driver,"ListAgentEmail",Listings_Dict,"DraftOther_SalesPersonEmail_1",exceptionDict,logger)

        salesperson2Brokerage=Listings_Dict["DraftOther_SalesPersonBrokerage_2"]
        salesperson2BrokerageField = driver.find_element(By.ID, "CoListOfficeKey")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", salesperson2BrokerageField)
        salesperson2BrokerageField.clear()
        salesperson2BrokerageField.send_keys(salesperson2Brokerage)
        time.sleep(2)

        salesperson2BrokerageOption = driver.find_element(By.XPATH,f"//mat-option[@role='option'][.//span[contains(normalize-space(), '{salesperson2Brokerage.strip()}')]]")
        driver.execute_script("arguments[0].click();", salesperson2BrokerageOption)
        time.sleep(1)
        
        fill_dropdown(driver,"CoListAgentKey",Listings_Dict,"DraftOther_SalesPerson_2",exceptionDict,logger)

        fill_textbox(driver,"CoListAgentDirectPhone",Listings_Dict,"DraftOther_SalesPersonPhone_2",exceptionDict,logger)

        fill_textbox(driver,"CoListAgentEmail",Listings_Dict,"DraftOther_SalesPersonEmail_2",exceptionDict,logger)

        salesperson3Brokerage=Listings_Dict["DraftOther_SalesPersonBrokerage_3"]
        salesperson3BrokerageField = driver.find_element(By.ID, "CoListOfficeKey3")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", salesperson3BrokerageField)
        salesperson3BrokerageField.clear()
        salesperson3BrokerageField.send_keys(salesperson3Brokerage)
        time.sleep(2)

        salesperson3BrokerageOption = driver.find_element(By.XPATH,f"//mat-option[@role='option'][.//span[contains(normalize-space(), '{salesperson3Brokerage.strip()}')]]")
        driver.execute_script("arguments[0].click();", salesperson3BrokerageOption)
        time.sleep(1)


        fill_dropdown(driver,"CoListAgent3Key",Listings_Dict,"DraftOther_SalesPerson_3",exceptionDict,logger)

        fill_textbox(driver,"CoListAgent3PreferredPhone",Listings_Dict,"DraftOther_SalesPersonPhone_3",exceptionDict,logger)

        fill_textbox(driver,"CoListAgent3Email",Listings_Dict,"DraftOther_SalesPersonEmail_3",exceptionDict,logger)

        salesperson4Brokerage=Listings_Dict["DraftOther_SalesPersonBrokerage_4"]
        salesperson4BrokerageField = driver.find_element(By.ID, "CoListOfficeKey4")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", salesperson4BrokerageField)
        salesperson4BrokerageField.clear()
        salesperson4BrokerageField.send_keys(salesperson4Brokerage)
        time.sleep(2)

        salesperson4BrokerageOption = driver.find_element(By.XPATH,f"//mat-option[@role='option'][.//span[contains(normalize-space(), '{salesperson4Brokerage.strip()}')]]")
        driver.execute_script("arguments[0].click();", salesperson4BrokerageOption)
        time.sleep(1)


        fill_dropdown(driver,"CoListAgent4Key",Listings_Dict,"DraftOther_SalesPerson_4",exceptionDict,logger)

        fill_textbox(driver,"CoListAgent4PreferredPhone",Listings_Dict,"DraftOther_SalesPersonPhone_3",exceptionDict,logger)

        fill_textbox(driver,"CoListAgent4Email",Listings_Dict,"DraftOther_SalesPersonEmail_4",exceptionDict,logger)

        

        fill_textbox(driver,"TransactionBrokerCompensation",Listings_Dict,"DraftOther_CommissionToCoOperatingBrokerage",exceptionDict,logger)

        fill_yesnobutton(driver,"VendorPropertyInfoStatement-true-button","VendorPropertyInfoStatement-false-button",Listings_Dict,"DraftOther_SellerPropertyInfoInformation",exceptionDict,logger)

        fill_yesnobutton(driver,"EnergyCertificate-true-button","EnergyCertificate-false-button",Listings_Dict,"DraftOther_EnergyCertificate",exceptionDict,logger)

        fill_textbox(driver,"GreenCertificationLevel",Listings_Dict,"DraftOther_CertificationLevel",exceptionDict,logger)

        fill_yesnobutton(driver,"GreenPropertyInformationStatement-true-button","GreenPropertyInformationStatement-false-button",Listings_Dict,"DraftOther_GreenPropertyInformationStatement",exceptionDict,logger)

        fill_yesnobutton(driver,"InternetEntireListingDisplayYN-true-button","InternetEntireListingDisplayYN-false-button",Listings_Dict,"DraftOther_DistributeToInternet",exceptionDict,logger)

        fill_yesnobutton(driver,"InternetAddressDisplayYN-true-button","InternetAddressDisplayYN-false-button",Listings_Dict,"DraftOther_DisplayAddressOnInternet",exceptionDict,logger)

        fill_yesnobutton(driver,"DDFYN-true-button","DDFYN-false-button",Listings_Dict,"DraftOther_DistributeToDDFIDX",exceptionDict,logger)

        fill_yesnobutton(driver,"PermissionToContactListingBrokerToAdvertise-true-button","PermissionToContactListingBrokerToAdvertise-false-button",Listings_Dict,"DraftOther_PermissionToContactListingBrokerToAdvertise",exceptionDict,logger)

        fill_yesnobutton(driver,"SignOnPropertyYN-true-button","SignOnPropertyYN-false-button",Listings_Dict,"DraftOther_RealtorSignOnProperty",exceptionDict,logger)

        fill_textbox(driver,"OpenHouseDate",Listings_Dict,"DraftOther_BrokerOpenHouseDateAndTime",exceptionDict,logger)

        startTimeButton = driver.find_element(By.XPATH,"//mat-label[normalize-space()='Start Time']/ancestor::mat-form-field//input[@role='combobox']")
        driver.execute_script("arguments[0].click();", startTimeButton)
        time.sleep(1)

        startTimeFieldButton = driver.find_element(By.XPATH,f"//mat-option[@role='option'][.//span[normalize-space()='{Listings_Dict['DraftOther_StartTime'].strip()}']]")
        driver.execute_script("arguments[0].click();", startTimeFieldButton)
        time.sleep(1)

        endTimeButton = driver.find_element(By.XPATH,"//mat-label[normalize-space()='End Time']/ancestor::mat-form-field//input[@role='combobox']")
        driver.execute_script("arguments[0].click();", endTimeButton)
        time.sleep(1)

        endTimeFieldButton = driver.find_element(By.XPATH,f"//mat-option[@role='option'][.//span[normalize-space()='{Listings_Dict['DraftOther_EndTime'].strip()}']]")
        driver.execute_script("arguments[0].click();", endTimeFieldButton)
        time.sleep(1)

        fill_textbox(driver,"ShowingAppointments",Listings_Dict,"DraftOther_AppointmentsShowingRemarks",exceptionDict,logger)

        fill_dropdown(driver,"OccupantType",Listings_Dict,"DraftOther_Occupancy",exceptionDict,logger)

        fill_combobox(driver,"ShowingRequirements",Listings_Dict,"DraftOther_ShowingRequirements",exceptionDict,logger)
        
        fill_yesnobutton(driver,"ContactAfterExpiryYN-true-button","ContactAfterExpiryYN-false-button",Listings_Dict,"DraftOther_ContactAfterExpired",exceptionDict,logger)

        fill_textbox(driver,"VirtualTourURLUnbranded",Listings_Dict,"DraftOther_UnbrandedVirtualTourURL1",exceptionDict,logger)

        fill_textbox(driver,"VirtualTourURLUnbranded2",Listings_Dict,"DraftOther_UnbrandedVirtualTourURL2",exceptionDict,logger)

        fill_textbox(driver,"VirtualTourURLBranded",Listings_Dict,"DraftOther_BrandedVirtualTourURL1",exceptionDict,logger)

        fill_textbox(driver,"VirtualTourURLBranded2",Listings_Dict,"DraftOther_BrandedVirtualTourURL2",exceptionDict,logger)

        fill_textbox(driver,"SalesBrochureUrl",Listings_Dict,"DraftOther_SalesBrochureURL",exceptionDict,logger)

        fill_textbox(driver,"AdditionalPicturesUrl",Listings_Dict,"DraftOther_AdditionalPicturesURL",exceptionDict,logger)

        fill_textbox(driver,"AlternateFeatureSheet",Listings_Dict,"DraftOther_AlternateFeatureSheetURL",exceptionDict,logger)

        fill_textbox(driver,"MapURL",Listings_Dict,"DraftOther_MapLocationURL",exceptionDict,logger)

        fill_textbox(driver,"SoundBiteUrl",Listings_Dict,"DraftOther_SoundBiteURL",exceptionDict,logger)
        
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
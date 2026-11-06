import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from screens.trebb_allfunctions import get_traceback, check_exceptiondict,fill_textbox,fill_dropdown,fill_yesnobutton,check_ui_errors

OVERLAY = "//div[contains(@class,'cdk-overlay-pane')]"

def draft_location_page(driver, Listings_Dict, exceptionDict, logger):
    try:
        WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.ID, "RollNumber")))
        # if Listings_Dict["DraftLocation_ARN"]:
        #     driver.find_element(By.ID, "RollNumber").clear()
        #     driver.find_element(By.ID, "RollNumber").send_keys(Listings_Dict["DraftLocation_ARN"])
        # else:
        #     noARNButton=driver.find_element(By.ID, "NoARNAvailableYN-input")
        #     driver.execute_script("arguments[0].click();", noARNButton)
        #     time.sleep(1)
        #     reasonNoARNField=driver.find_element(By.XPATH, "//input[@aria-label='Reason for No ARN']")
        #     driver.execute_script("arguments[0].click();", reasonNoARNField)
        #     time.sleep(1)
        #     driver.find_element(By.XPATH, OVERLAY + "//input[@aria-label='Search']").clear()
        #     driver.find_element(By.XPATH, OVERLAY + "//input[@aria-label='Search']").send_keys(Listings_Dict["DraftLocation_ReasonNoARN"])
        #     time.sleep(1)
        #     reasonNoARNFieldOption = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, OVERLAY + f"//mat-option[contains(normalize-space(.),'{Listings_Dict["DraftLocation_ReasonNoARN"]}')]")))
        #     driver.execute_script("arguments[0].click();", reasonNoARNFieldOption)
        #     time.sleep(1) 


        # if Listings_Dict["DraftLocation_PIN"]:
        #     driver.find_element(By.ID, "ParcelNumber").clear()
        #     driver.find_element(By.ID, "ParcelNumber").send_keys(Listings_Dict["DraftLocation_PIN"])
        # else:
        #     noPINButton=driver.find_element(By.ID, "NoPINAvailableYN-input")
        #     driver.execute_script("arguments[0].click();", noPINButton)
        #     time.sleep(1)
        #     reasonNoPINField=driver.find_element(By.XPATH, "//input[@aria-label='Reason No PIN']")
        #     driver.execute_script("arguments[0].click();", reasonNoPINField)
        #     time.sleep(1)
        #     driver.find_element(By.XPATH, OVERLAY + "//input[@aria-label='Search']").clear()
        #     driver.find_element(By.XPATH, OVERLAY + "//input[@aria-label='Search']").send_keys(Listings_Dict["DraftLocation_ReasonNoPIN"])
        #     time.sleep(1)
        #     reasonNoPINFieldOption = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, OVERLAY + f"//mat-option[contains(normalize-space(.),'{Listings_Dict["DraftLocation_ReasonNoPIN"]}')]")))
        #     driver.execute_script("arguments[0].click();", reasonNoPINFieldOption)
        #     time.sleep(1)
        draft_number = driver.find_element(By.CSS_SELECTOR, "div.listing-title span").text.replace("Draft", "").strip()
        logger.info(f"Draft Number Created - {draft_number}")
        
        fill_textbox(driver,"ParcelNumber2",Listings_Dict,"DraftLocation_AdditionalPIN",exceptionDict,logger)

        fill_dropdown(driver,"CountyOrParish",Listings_Dict,"DraftLocation_Area",exceptionDict,logger,searchMode=True,checkMode=True)

        fill_dropdown(driver,"City",Listings_Dict,"DraftLocation_Muncipality",exceptionDict,logger,searchMode=True,checkMode=True)

        fill_dropdown(driver,"CityRegion",Listings_Dict,"DraftLocation_Community",exceptionDict,logger,searchMode=True,checkMode=True)

        fill_dropdown(driver,"StreetDirPrefix",Listings_Dict,"DraftLocation_StreetDirectionPrefix",exceptionDict,logger,searchMode=True,checkMode=True)
        
        fill_textbox(driver,"StreetNumber",Listings_Dict,"DraftLocation_StreetNumber",exceptionDict,logger,checkMode=True)

        fill_textbox(driver,"StreetName",Listings_Dict,"DraftLocation_StreetName",exceptionDict,logger,checkMode=True)
        
        fill_dropdown(driver,"StreetSuffix",Listings_Dict,"DraftLocation_Abbreviation",exceptionDict,logger,searchMode=True,checkMode=True)

        fill_dropdown(driver,"StreetDirection",Listings_Dict,"DraftLocation_StreetDirSuffix",exceptionDict,logger)

        if Listings_Dict["Is_Condo"]:
            fill_textbox(driver,"UnitNumber",Listings_Dict,"DraftLocation_UnitNumber",exceptionDict,logger)

        fill_textbox(driver,"PostalCode",Listings_Dict,"DraftLocation_PostalCode",exceptionDict,logger,checkMode=True)

        if Listings_Dict["Is_Freehold"]:
            fill_dropdown(driver,"DirectionFaces",Listings_Dict,"DraftLocation_FrontingOn",exceptionDict,logger)
        
        if Listings_Dict["Is_Condo"]:
            fill_textbox(driver,"BuildingName",Listings_Dict,"DraftLocation_BuildingName",exceptionDict,logger)
            fill_textbox(driver,"AssociationName",Listings_Dict,"DraftLocation_CondoRegistryOffice",exceptionDict,logger)
            fill_textbox(driver,"CondoCorpNumber",Listings_Dict,"DraftLocation_CondoCorpNumber",exceptionDict,logger)
            fill_textbox(driver,"LegalStories",Listings_Dict,"DraftLocation_Level",exceptionDict,logger)
                        
        if Listings_Dict["Is_Commercial"] or (Listings_Dict["Is_Freehold"] and Listings_Dict["Is_ForSale"]):
            fill_textbox(driver,"TaxLegalDescription",Listings_Dict,"DraftLocation_LegalDescription",exceptionDict,logger)
                
        if not (Listings_Dict["Is_ForSale"] and (Listings_Dict["Is_Freehold"] or Listings_Dict["Is_Commercial"])):
            fill_textbox(driver,"PropertyManagementCompany",Listings_Dict,"DraftLocation_PropertyManagementCompany",exceptionDict,logger)

        if not Listings_Dict["Is_Condo"]:
            fill_textbox(driver,"LotWidth",Listings_Dict,"DraftLocation_LotFront",exceptionDict,logger)
            fill_textbox(driver,"LotDepth",Listings_Dict,"DraftLocation_LotDepth",exceptionDict,logger)
            fill_textbox(driver,"LotIrregularities",Listings_Dict,"DraftLocation_LotIrregularities",exceptionDict,logger)
            fill_dropdown(driver,"LotSizeUnits",Listings_Dict,"DraftLocation_LotSizeCode",exceptionDict,logger)
            
        if Listings_Dict["Is_Commercial"]:
            fill_dropdown(driver,"LotType",Listings_Dict,"DraftLocation_LotBuildingUnitCode",exceptionDict,logger)

        if Listings_Dict["DraftLocation_LotShape"]:
            if Listings_Dict["DraftLocation_LotShape"] not in ["Irregular","Pie","Rectangular","Reverse Pie","Square"]:
                Listings_Dict["DraftLocation_LotShape"]="Other"
            fill_dropdown(driver,"LotShape",Listings_Dict,"DraftLocation_LotShape",exceptionDict,logger)

        fill_dropdown(driver,"LotSizeSource",Listings_Dict,"DraftLocation_LotSizeSource",exceptionDict,logger)

        fill_textbox(driver,"LotSizeArea",Listings_Dict,"DraftLocation_LotSizeArea",exceptionDict,logger)

        fill_dropdown(driver,"LotSizeAreaUnits",Listings_Dict,"DraftLocation_LotSizeAreaCode",exceptionDict,logger)

        fill_dropdown(driver,"Winterized",Listings_Dict,"DraftLocation_Winterized",exceptionDict,logger)
        
        if Listings_Dict["Is_Freehold"]:             
            fill_dropdown(driver,"LotSizeRangeAcres",Listings_Dict,"DraftLocation_Acreage",exceptionDict,logger,searchMode=True)

        fill_yesnobutton(driver,"WaterfrontYN-true-button","WaterfrontYN-false-button",Listings_Dict,"DraftLocation_WaterFront",exceptionDict,logger)

        fill_textbox(driver,"Directions",Listings_Dict,"DraftLocation_Directions",exceptionDict,logger)
        
        fill_textbox(driver,"CrossStreet",Listings_Dict,"DraftLocation_MainCrossStreets",exceptionDict,logger)
        
        if Listings_Dict["Is_ForSale"] or Listings_Dict["Is_Commercial"]:
            fill_textbox(driver,"Zoning",Listings_Dict,"DraftLocation_Zoning",exceptionDict,logger)

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
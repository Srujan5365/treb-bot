import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from selenium.webdriver.common.keys import Keys
from screens.trebb_allfunctions import get_traceback, check_exceptiondict,fill_dropdown,fill_textbox,fill_yesnobutton,fill_combobox,check_ui_errors


def draft_waterfrontrural_page(driver, Listings_Dict, exceptionDict, logger):
    try:

        fill_combobox(driver,"Waterfront",Listings_Dict,"DraftWaterfrontRural_WaterfrontType",exceptionDict,logger)
        fill_dropdown(driver,"WaterBodyName",Listings_Dict,"DraftWaterfrontRural_BodyOfWaterName",exceptionDict,logger,searchMode=True)
        fill_dropdown(driver,"WaterBodyType",Listings_Dict,"DraftWaterfrontRural_WaterBodyType",exceptionDict,logger,searchMode=True) 
        fill_yesnobutton(driver,"IslandYN-true-button","IslandYN-false-button",Listings_Dict,"DraftWaterfrontRural_Island",exceptionDict,logger)
        fill_combobox(driver,"WaterView",Listings_Dict,"DraftWaterfrontRural_WaterView",exceptionDict,logger)
        fill_textbox(driver,"ChannelName",Listings_Dict,"DraftWaterfrontRural_ChannelName",exceptionDict,logger) 
        fill_textbox(driver,"WaterFrontage",Listings_Dict,"DraftWaterfrontRural_WaterFrontage",exceptionDict,logger) 
        fill_dropdown(driver,"WaterFrontageUnits",Listings_Dict,"DraftWaterfrontRural_WaterFrontageUnits",exceptionDict,logger)
        fill_yesnobutton(driver,"SeasonalDwelling-true-button","SeasonalDwelling-false-button",Listings_Dict,"DraftWaterfrontRural_SeasonalDwelling",exceptionDict,logger)
        fill_combobox(driver,"AccessToProperty",Listings_Dict,"DraftWaterfrontRural_AccessToProperty",exceptionDict,logger,searchMode=True,expandButtonName="Access to Property")
        fill_combobox(driver,"Shoreline",Listings_Dict,"DraftWaterfrontRural_Shoreline",exceptionDict,logger,searchMode=True,expandButtonName="Shoreline")
        fill_combobox(driver,"WaterfrontFeatures",Listings_Dict,"DraftWaterfrontRural_WaterfrontFeatures",exceptionDict,logger,searchMode=True,expandButtonName="Waterfront Features")
        fill_combobox(driver,"ShorelineExposureMulti",Listings_Dict,"DraftWaterfrontRural_ShorelineExposure",exceptionDict,logger)
        fill_dropdown(driver,"ShorelineAllowance",Listings_Dict,"DraftWaterfrontRural_ShorelineAllowance",exceptionDict,logger) 
        fill_combobox(driver,"AlternativePower",Listings_Dict,"DraftWaterfrontRural_AlternativePower",exceptionDict,logger)
        fill_combobox(driver,"Sewage",Listings_Dict,"DraftWaterfrontRural_Sewage",exceptionDict,logger)
        fill_combobox(driver,"WaterDeliveryFeature",Listings_Dict,"DraftWaterfrontRural_WaterDeliveryFeatures",exceptionDict,logger)
        #fill_combobox(driver,"ShorelineExposure",Listings_Dict,"DraftWaterfrontRural_ShorelineExposure",exceptionDict,logger,searchMode=True)
        fill_combobox(driver,"Disclosures",Listings_Dict,"DraftWaterfrontRural_EasementsRestrictions",exceptionDict,logger,searchMode=True,expandButtonName="Easements/ Restrictions")
        fill_combobox(driver,"RuralUtilities",Listings_Dict,"DraftWaterfrontRural_RuralServices",exceptionDict,logger,searchMode=True,expandButtonName="Rural Services")
        fill_combobox(driver,"WaterfrontAccessory",Listings_Dict,"DraftWaterfrontRural_WaterfrontAccessoryBuildings",exceptionDict,logger,searchMode=True,expandButtonName="Waterfront Accessory Buildings")
        #fill_combobox(driver,"ShorelineExposure",Listings_Dict,"DraftWaterfrontRural_ShorelineExposure",exceptionDict,logger,searchMode=True)
        fill_combobox(driver,"DockingType",Listings_Dict,"DraftWaterfrontRural_DockingType",exceptionDict,logger) 
                       
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
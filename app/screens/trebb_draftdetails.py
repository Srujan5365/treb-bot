import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from selenium.webdriver.common.keys import Keys
from screens.trebb_allfunctions import get_traceback, check_exceptiondict,fill_dropdown,fill_textbox,fill_yesnobutton,fill_combobox,check_ui_errors


def draft_details_page(driver, Listings_Dict, exceptionDict, logger):
    try:
        fill_dropdown(driver,"PropertySubType",Listings_Dict,"DraftDetails_Type",exceptionDict,logger,searchMode=True)
        fill_dropdown(driver,"PropertyUse",Listings_Dict,"DraftDetails_Category",exceptionDict,logger)
        fill_dropdown(driver,"BusinessType",Listings_Dict,"DraftDetails_Use",exceptionDict,logger)   
        fill_yesnobutton(driver,"FreestandingYN-true-button","FreestandingYN-false-button",Listings_Dict,"DraftDetails_Freestanding",exceptionDict,logger)
        fill_textbox(driver,"BuildingAreaTotal",Listings_Dict,"DraftDetails_TotalArea",exceptionDict,logger)
        fill_dropdown(driver,"BuildingAreaUnits",Listings_Dict,"DraftDetails_TotalAreaCode",exceptionDict,logger)
                
        fill_textbox(driver,"PercentBuilding",Listings_Dict,"DraftDetails_PercentBuilding",exceptionDict,logger)  
        fill_textbox(driver,"OfficeApartmentArea",Listings_Dict,"DraftDetails_OfficeApartmentArea",exceptionDict,logger)
        fill_dropdown(driver,"OfficeApartmentAreaUnit",Listings_Dict,"DraftDetails_OfficeApartmentAreaCode",exceptionDict,logger)
        
        fill_textbox(driver,"IndustrialArea",Listings_Dict,"DraftDetails_IndustrialArea",exceptionDict,logger)
        fill_dropdown(driver,"IndustrialAreaCode",Listings_Dict,"DraftDetails_IndustrialAreaCode",exceptionDict,logger)
        fill_textbox(driver,"RetailArea",Listings_Dict,"DraftDetails_RetailArea",exceptionDict,logger) 
        fill_dropdown(driver,"RetailAreaCode",Listings_Dict,"DraftDetails_RetailAreaCode",exceptionDict,logger)
        fill_dropdown(driver,"ApproximateAge",Listings_Dict,"DraftDetails_ApproximateAge",exceptionDict,logger)
        fill_combobox(driver,"CommunityFeatures",Listings_Dict,"DraftDetails_AreaInfluences",exceptionDict,logger)
        fill_yesnobutton(driver,"HandicappedEquippedYN-true-button","HandicappedEquippedYN-false-button",Listings_Dict,"DraftDetails_PhysicallyHandicappedEquipped",exceptionDict,logger)
        fill_yesnobutton(driver,"BasementYN-true-button","BasementYN-false-button",Listings_Dict,"DraftDetails_Basement",exceptionDict,logger)
        fill_dropdown(driver,"UFFI",Listings_Dict,"DraftDetails_UFFI",exceptionDict,logger)
        
        fill_textbox(driver,"ClearHeightFeet",Listings_Dict,"DraftDetails_ClearHeightFeet",exceptionDict,logger)
        fill_textbox(driver,"ClearHeightInches",Listings_Dict,"DraftDetails_ClearHeightInches",exceptionDict,logger)
        fill_combobox(driver,"SecurityFeatures",Listings_Dict,"DraftDetails_Sprinklers",exceptionDict,logger)
        fill_dropdown(driver,"Utilities",Listings_Dict,"DraftDetails_Utilities",exceptionDict,logger)
        
        fill_textbox(driver,"BaySizeWidthFeet",Listings_Dict,"DraftDetails_BaySizeWidthFeet",exceptionDict,logger)
        fill_textbox(driver,"BaySizeWidthInches",Listings_Dict,"DraftDetails_BaySizeWidthInches",exceptionDict,logger)
        fill_textbox(driver,"BaySizeLengthFeet",Listings_Dict,"DraftDetails_BaySizeLengthFeet",exceptionDict,logger)
        fill_textbox(driver,"BaySizeLengthInches",Listings_Dict,"DraftDetails_BaySizeLengthInches",exceptionDict,logger)
        fill_textbox(driver,"Amps",Listings_Dict,"DraftDetails_BaySizeAmps",exceptionDict,logger)
        fill_textbox(driver,"Volts",Listings_Dict,"DraftDetails_BaySizeVolts",exceptionDict,logger)
        fill_dropdown(driver,"Water",Listings_Dict,"DraftDetails_BaySizeWater",exceptionDict,logger)
        fill_combobox(driver,"WaterSource",Listings_Dict,"DraftDetails_BaySizeWaterSupplyType",exceptionDict,logger,searchMode=True,expandButtonName="Water Supply Type")
        fill_combobox(driver,"Cooling",Listings_Dict,"DraftDetails_BaySizeAirConditioning",exceptionDict,logger)
        fill_combobox(driver,"HeatTypeMulti",Listings_Dict,"DraftDetails_BaySizeHeatType",exceptionDict,logger,searchMode=True,expandButtonName="Heat Type")
        fill_textbox(driver,"WashroomsType1",Listings_Dict,"DraftDetails_BaySizeWashrooms",exceptionDict,logger)
        
        fill_textbox(driver,"TruckLevelShippingDoors",Listings_Dict,"DraftDetails_TruckLevelShippingDoors",exceptionDict,logger)
        fill_textbox(driver,"TruckLevelShippingDoorsHeightFeet",Listings_Dict,"DraftDetails_TrucklevelDoorsHeightFeet",exceptionDict,logger)
        fill_textbox(driver,"TruckLevelShippingDoorsHeightInches",Listings_Dict,"DraftDetails_TrucklevelDoorsHeightInches",exceptionDict,logger)
        fill_textbox(driver,"TruckLevelShippingDoorsWidthFeet",Listings_Dict,"DraftDetails_TrucklevelDoorsWidthFeet",exceptionDict,logger)
        fill_textbox(driver,"TruckLevelShippingDoorsWidthInches",Listings_Dict,"DraftDetails_TrucklevelDoorsWidthInches",exceptionDict,logger)
        fill_textbox(driver,"DoubleManShippingDoors",Listings_Dict,"DraftDetails_TrucklevelDoubleManShippingDoors",exceptionDict,logger)
        
        fill_textbox(driver,"DoubleManShippingDoorsHeightFeet",Listings_Dict,"DraftDetails_DoubleManDoorsHeightFeet",exceptionDict,logger)
        fill_textbox(driver,"DoubleManShippingDoorsHeightInches",Listings_Dict,"DraftDetails_DoubleManDoorsHeightInches",exceptionDict,logger)
        fill_textbox(driver,"DoubleManShippingDoorsWidthFeet",Listings_Dict,"DraftDetails_DoubleManDoorsWidthFeet",exceptionDict,logger)
        fill_textbox(driver,"DoubleManShippingDoorsWidthInches",Listings_Dict,"DraftDetails_DoubleManDoorsWidthInches",exceptionDict,logger)
        
        
        fill_textbox(driver,"DriveInLevelShippingDoors",Listings_Dict,"DraftDetails_DriveInLevelShippingDoors",exceptionDict,logger)
        fill_textbox(driver,"DriveInLevelShippingDoorsHeightFeet",Listings_Dict,"DraftDetails_DriveInDoorsHeightFeet",exceptionDict,logger)
        fill_textbox(driver,"DriveInLevelShippingDoorsHeightInches",Listings_Dict,"DraftDetails_DriveInDoorsHeightInches",exceptionDict,logger)
        fill_textbox(driver,"DriveInLevelShippingDoorsWidthFeet",Listings_Dict,"DraftDetails_DriveInDoorsWidthFeet",exceptionDict,logger)
        fill_textbox(driver,"DriveInLevelShippingDoorsWidthInches",Listings_Dict,"DraftDetails_DriveInDoorsWidthInches",exceptionDict,logger)
        
        fill_textbox(driver,"GradeLevelShippingDoors",Listings_Dict,"DraftDetails_GradeLevelShippingDoors",exceptionDict,logger)
        fill_textbox(driver,"GradeLevelShippingDoorsHeightFeet",Listings_Dict,"DraftDetails_GradeLevelDoorsHeightFeet",exceptionDict,logger)
        fill_textbox(driver,"GradeLevelShippingDoorsHeightInches",Listings_Dict,"DraftDetails_GradeLevelDoorsHeightInches",exceptionDict,logger)
        fill_textbox(driver,"GradeLevelShippingDoorsWidthFeet",Listings_Dict,"DraftDetails_GradeLevelDoorsWidthFeet",exceptionDict,logger)
        fill_textbox(driver,"GradeLevelShippingDoorsWidthInches",Listings_Dict,"DraftDetails_GradeLevelDoorsWidthInches",exceptionDict,logger)
        
        
        fill_dropdown(driver,"ElevatorType",Listings_Dict,"DraftDetails_Elevator",exceptionDict,logger)
        fill_dropdown(driver,"GarageType",Listings_Dict,"DraftDetails_GarageType",exceptionDict,logger,searchMode=True)
        fill_textbox(driver,"ParkingSpaces",Listings_Dict,"DraftDetails_ParkingSpaces",exceptionDict,logger)
        fill_textbox(driver,"TrailerParkingSpots",Listings_Dict,"DraftDetails_NumberofTrailerParkingSpots",exceptionDict,logger)
        
        fill_yesnobutton(driver,"OutsideStorageYN-true-button","OutsideStorageYN-false-button",Listings_Dict,"DraftDetails_OutsideStorage",exceptionDict,logger)
        fill_dropdown(driver,"Rail",Listings_Dict,"DraftDetails_Rail",exceptionDict,logger)
        fill_yesnobutton(driver,"CraneYN-true-button","CraneYN-false-button",Listings_Dict,"DraftDetails_Crane",exceptionDict,logger)
        fill_yesnobutton(driver,"SurveyAvailableYN-true-button","SurveyAvailableYN-false-button",Listings_Dict,"DraftDetails_Survey",exceptionDict,logger)
        fill_dropdown(driver,"SoilTest",Listings_Dict,"DraftDetails_SoilTest",exceptionDict,logger)
        fill_dropdown(driver,"Sewer",Listings_Dict,"DraftDetails_Sewers",exceptionDict,logger,searchMode=True)
        
        fill_combobox(driver,"FarmFeatures",Listings_Dict,"DraftDetails_FarmFeatures",exceptionDict,logger,searchMode=True,expandButtonName="View")        
        fill_textbox(driver,"YearBuilt",Listings_Dict,"DraftDetails_YearBuilt",exceptionDict,logger)
        fill_dropdown(driver,"YearBuiltSource",Listings_Dict,"DraftDetails_YearBuiltSource",exceptionDict,logger,searchMode=True)
                   
                
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
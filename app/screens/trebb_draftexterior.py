import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from selenium.webdriver.common.keys import Keys
from screens.trebb_allfunctions import get_traceback, check_exceptiondict,fill_dropdown,fill_textbox,fill_yesnobutton,fill_combobox,check_ui_errors


def draft_exterior_page(driver, Listings_Dict, exceptionDict, logger):
    try:
        fill_dropdown(driver,"PropertySubType",Listings_Dict,"DraftExterior_PropertyType",exceptionDict,logger,searchMode=True)
        if Listings_Dict["DraftExterior_PropertyType"]=="Detached":
            fill_yesnobutton(driver,"LinkYN-true-button","LinkYN-false-button",Listings_Dict,"DraftExterior_LINK",exceptionDict,logger)
        if Listings_Dict["Is_Freehold"]:
            fill_yesnobutton(driver,"ParcelOfTiedLand-Yes-button","ParcelOfTiedLand-No-button",Listings_Dict,"DraftExterior_ParcelofTiedLand",exceptionDict,logger) 
            if Listings_Dict.get("DraftExterior_ParcelofTiedLand","No")=="Yes":
                fill_textbox(driver,"AdditionalMonthlyFee",Listings_Dict,"DraftExterior_POTLMonthlyFee",exceptionDict,logger)
            fill_yesnobutton(driver,"VacantLandCondoYN-true-button","VacantLandCondoYN-false-button",Listings_Dict,"DraftExterior_VacantLandCondo",exceptionDict,logger)
            if Listings_Dict.get("DraftExterior_VacantLandCondo","No")=="Yes":
                fill_textbox(driver,"VacantLandCondoFee",Listings_Dict,"DraftExterior_VacantLandCondoMonthlyFee",exceptionDict,logger)
        
            
        if Listings_Dict["Is_ForSale"]:
            fill_yesnobutton(driver,"AssignmentYN-true-button","AssignmentYN-false-button",Listings_Dict,"DraftExterior_Assignment",exceptionDict,logger)
            fill_yesnobutton(driver,"FractionalOwnershipYN-true-button","FractionalOwnershipYN-false-button",Listings_Dict,"DraftExterior_FractionalOwnership",exceptionDict,logger)
        
        if not Listings_Dict["Is_ForSale"]:
            fill_combobox(driver,"PortionPropertyLease",Listings_Dict,"DraftExterior_PortionofPropertyforLease",exceptionDict,logger,searchMode=True)
            fill_textbox(driver,"PortionLeaseComments",Listings_Dict,"DraftExterior_PortionofPropertyComments",exceptionDict,logger)
        
        #present for all 
        fill_dropdown(driver,"ArchitecturalStyle",Listings_Dict,"DraftExterior_Style",exceptionDict,logger,searchMode=True)       
        fill_combobox(driver,"View",Listings_Dict,"DraftExterior_View",exceptionDict,logger,searchMode=True,expandButtonName="View")
        fill_combobox(driver,"ConstructionMaterials",Listings_Dict,"DraftExterior_Exterior",exceptionDict,logger,searchMode=True,expandButtonName="Exterior")
        fill_combobox(driver,"ExteriorFeatures",Listings_Dict,"DraftExterior_ExteriorFeatures",exceptionDict,logger,searchMode=True,expandButtonName="Exterior Features")
        fill_combobox(driver,"FoundationDetails",Listings_Dict,"DraftExterior_FoundationDetail",exceptionDict,logger,searchMode=True,expandButtonName="Foundation Detail")
        fill_combobox(driver,"Roof",Listings_Dict,"DraftExterior_Roof",exceptionDict,logger,searchMode=True,expandButtonName="Roof")
        fill_combobox(driver,"Topography",Listings_Dict,"DraftExterior_Topography",exceptionDict,logger,searchMode=True,expandButtonName="Topography")
        fill_yesnobutton(driver,"GarageYN-true-button","GarageYN-false-button",Listings_Dict,"DraftExterior_Garage",exceptionDict,logger)
        fill_dropdown(driver,"GarageType",Listings_Dict,"DraftExterior_GarageType",exceptionDict,logger,searchMode=True)  
        fill_textbox(driver,"CoveredSpaces",Listings_Dict,"DraftExterior_GarageParkingSpaces",exceptionDict,logger)
        fill_combobox(driver,"ParkingFeatures",Listings_Dict,"DraftExterior_ParkingDrive",exceptionDict,logger,searchMode=True,expandButtonName="Parking/Drive")
        fill_textbox(driver,"ParkingSpaces",Listings_Dict,"DraftExterior_DriveParkingSpaces",exceptionDict,logger)
        fill_textbox(driver,"ParkingTotal",Listings_Dict,"DraftExterior_TotalParkingSpaces",exceptionDict,logger)
            
        if Listings_Dict["Is_Condo"]:
            #Parking Type 1
            fill_dropdown(driver,"ParkingType1",Listings_Dict,"DraftExterior_ParkingType1",exceptionDict,logger)
            #Parking Level/Unit 1
            fill_textbox(driver,"ParkingLevelUnit1",Listings_Dict,"DraftExterior_ParkingLevelUnit1",exceptionDict,logger)
            #Parking Spot 1
            fill_textbox(driver,"ParkingSpot1",Listings_Dict,"DraftExterior_ParkingSpot1",exceptionDict,logger)
            #Parking Type 2
            fill_dropdown(driver,"ParkingType2",Listings_Dict,"DraftExterior_ParkingType2",exceptionDict,logger)
            #Parking Level/Unit 2
            fill_textbox(driver,"ParkingLevelUnit2",Listings_Dict,"DraftExterior_ParkingLevelUnit2",exceptionDict,logger)
            #Parking Spot 2
            fill_textbox(driver,"ParkingSpot2",Listings_Dict,"DraftExterior_ParkingSpot2",exceptionDict,logger)
            #Parking Cost/Month
            fill_textbox(driver,"ParkingMonthlyCost",Listings_Dict,"DraftExterior_ParkingCostMonth",exceptionDict,logger)
            #Exposure
            fill_dropdown(driver,"Exposure",Listings_Dict,"DraftExterior_Exposure",exceptionDict,logger)
            fill_dropdown(driver,"BalconyType",Listings_Dict,"DraftExterior_Balcony",exceptionDict,logger)
            
        if Listings_Dict["Is_Freehold"]:
            fill_dropdown(driver,"Water",Listings_Dict,"DraftExterior_Water",exceptionDict,logger)  
            fill_combobox(driver,"PoolFeatures",Listings_Dict,"DraftExterior_Pool",exceptionDict,logger,searchMode=True,expandButtonName="Pool")
            fill_dropdown(driver,"Sewer",Listings_Dict,"DraftExterior_Sewers",exceptionDict,logger)  
            
        #presentforall  
        fill_yesnobutton(driver,"SeniorCommunityYN-true-button","SeniorCommunityYN-false-button",Listings_Dict,"DraftExterior_RetirementCommunity",exceptionDict,logger)
        fill_yesnobutton(driver,"HandicappedEquippedYN-true-button","HandicappedEquippedYN-false-button",Listings_Dict,"DraftExterior_PhysicallyHandicappedEquipped",exceptionDict,logger)
        fill_combobox(driver,"SpecialDesignation",Listings_Dict,"DraftExterior_SpecialDesignation",exceptionDict,logger)
        fill_dropdown(driver,"ApproximateAge",Listings_Dict,"DraftExterior_ApproximateAge",exceptionDict,logger)
        fill_textbox(driver,"YearBuilt",Listings_Dict,"DraftExterior_YearBuilt",exceptionDict,logger)
        fill_dropdown(driver,"YearBuiltSource",Listings_Dict,"DraftExterior_YearBuiltSource",exceptionDict,logger)
        fill_textbox(driver,"BuilderName",Listings_Dict,"DraftExterior_Builder",exceptionDict,logger)
        fill_dropdown(driver,"LivingAreaRange",Listings_Dict,"DraftExterior_ApproximateSquareFootage",exceptionDict,logger,searchMode=True) 
        
        if Listings_Dict["Is_Condo"]:
            fill_textbox(driver,"SquareFootSource",Listings_Dict,"DraftExterior_SQFTSourceComment",exceptionDict,logger)
        
        #present for all
        fill_textbox(driver,"AboveGradeFinishedArea",Listings_Dict,"DraftExterior_AboveGradeFinishedSQFT",exceptionDict,logger)
        fill_dropdown(driver,"AboveGradeFinishedAreaSource",Listings_Dict,"DraftExterior_AboveGradeFinishedSQFTSource",exceptionDict,logger,searchMode=True)
        fill_textbox(driver,"BelowGradeFinishedArea",Listings_Dict,"DraftExterior_BelowGradeFinishedSQFT",exceptionDict,logger)
        fill_dropdown(driver,"BelowGradeFinishedAreaSource",Listings_Dict,"DraftExterior_BelowGradeFinishedSQFTSource",exceptionDict,logger,searchMode=True)
        fill_textbox(driver,"OtherArea",Listings_Dict,"DraftExterior_OtherSQFT",exceptionDict,logger)
        fill_textbox(driver,"TotalUnfinishedArea",Listings_Dict,"DraftExterior_TotalUnfinished",exceptionDict,logger)
        fill_combobox(driver,"PropertyFeatures",Listings_Dict,"DraftExterior_PropertyFeaturesAreaInfluences",exceptionDict,logger,searchMode=True,expandButtonName="Property Features/ Area Influences")
        fill_combobox(driver,"SecurityFeatures",Listings_Dict,"DraftExterior_SecurityFeatures",exceptionDict,logger,searchMode=True,expandButtonName="Security Features")
            
        if Listings_Dict["Is_Freehold"]:
            fill_combobox(driver,"OtherStructures",Listings_Dict,"DraftExterior_OtherStructures",exceptionDict,logger,searchMode=True,expandButtonName="Other Structures")
        
        
        if Listings_Dict["Is_Condo"]:
            fill_combobox(driver,"BuildingAmenities",Listings_Dict,"DraftExterior_BuildingAmenities",exceptionDict,logger,searchMode=True,expandButtonName= "Building Amenities" )
            
            
            
            
        if Listings_Dict["Is_Freehold"]:
            fill_combobox(driver,"WaterSource",Listings_Dict,"DraftExterior_WaterSupplyType",exceptionDict,logger,searchMode=True,expandButtonName="Water Supply Type")
            fill_combobox(driver,"FarmType",Listings_Dict,"DraftExterior_Farm/Agriculture",exceptionDict,logger,searchMode=True,expandButtonName="Farm/ Agriculture")
            fill_combobox(driver,"FarmFeatures",Listings_Dict,"DraftExterior_FarmFeatures",exceptionDict,logger,searchMode=True,expandButtonName="Farm Features")
            fill_combobox(driver,"SoilType",Listings_Dict,"DraftExterior_SoilType",exceptionDict,logger,searchMode=True,expandButtonName="Soil Type")
        
        #present for all 
        fill_dropdown(driver,"SurveyType",Listings_Dict,"DraftExterior_SurveyType",exceptionDict,logger)
        fill_dropdown(driver,"SurveyYear",Listings_Dict,"DraftExterior_SurveyYear",exceptionDict,logger)
        
        if Listings_Dict["Is_ForSale"]:
            fill_yesnobutton(driver,"WaterMeterYN-true-button","WaterMeterYN-false-button",Listings_Dict,"DraftExterior_WaterMeter",exceptionDict,logger)
        if Listings_Dict["Is_Freehold"]:
            fill_textbox(driver,"WellCapacity",Listings_Dict,"DraftExterior_WellCapacityGalMinute",exceptionDict,logger)
            fill_textbox(driver,"WellDepth",Listings_Dict,"DraftExterior_WellDepth",exceptionDict,logger)
            fill_dropdown(driver,"CableYNA",Listings_Dict,"DraftExterior_Cable",exceptionDict,logger)
            fill_dropdown(driver,"ElectricYNA",Listings_Dict,"DraftExterior_Hydro",exceptionDict,logger)
            fill_dropdown(driver,"SewerYNA",Listings_Dict,"DraftExterior_SewersYN",exceptionDict,logger)
            fill_dropdown(driver,"GasYNA",Listings_Dict,"DraftExterior_Gas(Natural)",exceptionDict,logger)
            fill_dropdown(driver,"WaterYNA",Listings_Dict,"DraftExterior_MunicipalWater",exceptionDict,logger)
            fill_dropdown(driver,"TelephoneYNA",Listings_Dict,"DraftExterior_Telephone",exceptionDict,logger)      
                       
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
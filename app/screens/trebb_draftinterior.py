import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from selenium.webdriver.common.keys import Keys
from screens.trebb_allfunctions import get_traceback, check_exceptiondict,fill_dropdown,fill_textbox,fill_yesnobutton,fill_combobox,check_ui_errors


def draft_interior_page(driver, Listings_Dict, exceptionDict, logger):
    try:

        #fill_dropdown(driver,"",Listings_Dict,"",exceptionDict,logger)
        #fill_textbox(driver,"",Listings_Dict,"",exceptionDict,logger)
        #fill_yesnobutton(driver,"","",Listings_Dict,"",exceptionDict,logger)
        #fill_combobox(driver,"",Listings_Dict,"",exceptionDict,logger,searchMode=True)

        
        fill_textbox(driver,"RoomsAboveGrade",Listings_Dict,"DraftInterior_NumberofRooms",exceptionDict,logger)
        fill_textbox(driver,"RoomsBelowGrade",Listings_Dict,"DraftInterior_RoomsPlus",exceptionDict,logger)
        fill_textbox(driver,"BedroomsAboveGrade",Listings_Dict,"DraftInterior_NumberofBedrooms",exceptionDict,logger)
        fill_textbox(driver,"BedroomsBelowGrade",Listings_Dict,"DraftInterior_BedroomsPlus",exceptionDict,logger)
        fill_textbox(driver,"KitchensAboveGrade",Listings_Dict,"DraftInterior_NumberofKitchens",exceptionDict,logger)
        fill_textbox(driver,"KitchensBelowGrade",Listings_Dict,"DraftInterior_KitchensPlus",exceptionDict,logger)
        
        fill_textbox(driver,"WashroomsType1",Listings_Dict,"DraftInterior_Washrooms1",exceptionDict,logger)
        fill_textbox(driver,"WashroomsType1Pcs",Listings_Dict,"DraftInterior_NumberOfPieces1",exceptionDict,logger)
        fill_dropdown(driver,"WashroomsType1Level",Listings_Dict,"DraftInterior_Level1",exceptionDict,logger,searchMode=True)
        
        fill_textbox(driver,"WashroomsType2",Listings_Dict,"DraftInterior_Washrooms2",exceptionDict,logger)
        fill_textbox(driver,"WashroomsType2Pcs",Listings_Dict,"DraftInterior_NumberOfPieces2",exceptionDict,logger)
        fill_dropdown(driver,"WashroomsType2Level",Listings_Dict,"DraftInterior_Level2",exceptionDict,logger,searchMode=True)
        
        fill_textbox(driver,"WashroomsType3",Listings_Dict,"DraftInterior_Washrooms3",exceptionDict,logger)
        fill_textbox(driver,"WashroomsType3Pcs",Listings_Dict,"DraftInterior_NumberOfPieces3",exceptionDict,logger)
        fill_dropdown(driver,"WashroomsType3Level",Listings_Dict,"DraftInterior_Level3",exceptionDict,logger,searchMode=True)
        
        fill_textbox(driver,"WashroomsType4",Listings_Dict,"DraftInterior_Washrooms4",exceptionDict,logger)
        fill_textbox(driver,"WashroomsType4Pcs",Listings_Dict,"DraftInterior_NumberOfPieces4",exceptionDict,logger)
        fill_dropdown(driver,"WashroomsType4Level",Listings_Dict,"DraftInterior_Level4",exceptionDict,logger,searchMode=True)
        
        fill_textbox(driver,"WashroomsType5",Listings_Dict,"DraftInterior_Washrooms5",exceptionDict,logger)
        fill_textbox(driver,"WashroomsType5Pcs",Listings_Dict,"DraftInterior_NumberOfPieces5",exceptionDict,logger)
        fill_dropdown(driver,"WashroomsType5Level",Listings_Dict,"DraftInterior_Level5",exceptionDict,logger,searchMode=True)

        
        
        fill_combobox(driver,"InteriorFeatures",Listings_Dict,"DraftInterior_InteriorFeatures",exceptionDict,logger,searchMode=True,expandButtonName="Interior Features")
        fill_yesnobutton(driver,"DenFamilyroomYN-true-button","DenFamilyroomYN-false-button",Listings_Dict,"DraftInterior_FamilyRoomBonusRoom",exceptionDict,logger)
        fill_combobox(driver,"Basement",Listings_Dict,"DraftInterior_Basement",exceptionDict,logger,searchMode=True,expandButtonName="Basement")
        fill_yesnobutton(driver,"FireplaceYN-true-button","FireplaceYN-false-button",Listings_Dict,"DraftInterior_FireplaceStove",exceptionDict,logger)
        fill_combobox(driver,"FireplaceFeatures",Listings_Dict,"DraftInterior_FireplaceFeatures",exceptionDict,logger,searchMode=True,expandButtonName="Fireplace Features")
        fill_textbox(driver,"FireplacesTotal",Listings_Dict,"DraftInterior_NumberofFireplaces",exceptionDict,logger)
        fill_combobox(driver,"HeatSourceMulti",Listings_Dict,"DraftInterior_HeatSource",exceptionDict,logger)
        fill_combobox(driver,"HeatTypeMulti",Listings_Dict,"DraftInterior_HeatType",exceptionDict,logger)
        fill_combobox(driver,"Cooling",Listings_Dict,"DraftInterior_AirConditioning",exceptionDict,logger)

        if Listings_Dict["Is_Condo"]:
            fill_dropdown(driver,"PetsAllowed",Listings_Dict,"DraftInterior_PetsPermitted",exceptionDict,logger)

        fill_dropdown(driver,"UFFI",Listings_Dict,"DraftInterior_UFFI",exceptionDict,logger)              
        fill_dropdown(driver,"LaundryLevel",Listings_Dict,"DraftInterior_LaundryLevel",exceptionDict,logger)

        if not (Listings_Dict["Is_ForSale"] and Listings_Dict["Is_Freehold"]):
            fill_combobox(driver,"LaundryFeatures",Listings_Dict,"DraftInterior_LaundryFeatures",exceptionDict,logger,searchMode=True,expandButtonName="Laundry Features")
                    
        fill_combobox(driver,"AccessibilityFeatures",Listings_Dict,"DraftInterior_AccessibilityFeatures",exceptionDict,logger,searchMode=True,expandButtonName="Accessibility Features")
        fill_yesnobutton(driver,"ElevatorYN-true-button","ElevatorYN-false-button",Listings_Dict,"DraftInterior_ElevatorLift",exceptionDict,logger)

        if not (Listings_Dict["Is_ForSale"]):
            fill_dropdown(driver,"Furnished",Listings_Dict,"DraftInterior_Furnished",exceptionDict,logger,searchMode=True)
        
        if Listings_Dict["Is_Condo"]:
            fill_dropdown(driver,"Locker",Listings_Dict,"DraftInterior_Locker",exceptionDict,logger)
            fill_textbox(driver,"LockerLevel",Listings_Dict,"DraftInterior_LockerLevel",exceptionDict,logger)
            fill_textbox(driver,"LockerUnit",Listings_Dict,"DraftInterior_LockerUnit",exceptionDict,logger)
            fill_textbox(driver,"LockerNumber",Listings_Dict,"DraftInterior_LockerNumber",exceptionDict,logger)
                           
        if Listings_Dict["Is_ForSale"]:
            fill_combobox(driver,"LeaseToOwnEquipment",Listings_Dict,"DraftInterior_LeaseToOwnItems",exceptionDict,logger)
            fill_combobox(driver,"UnderContract",Listings_Dict,"DraftInterior_UnderContract",exceptionDict,logger,searchMode=True,expandButtonName="Under Contract")
        
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
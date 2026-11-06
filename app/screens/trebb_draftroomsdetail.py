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


def draft_roomsdetail_page(driver, Listings_Dict, exceptionDict, logger):
    try:
        for roomNumber in range(1,int(Listings_Dict["DraftRoomsDetail_NumberOfRooms"])+1):
            
            if len(driver.find_elements(By.XPATH, '//mat-select[@id="PropertyRooms[].RoomLevel"]')) < roomNumber:
                addAnotherRoom=driver.find_element(By.XPATH, "//button[.//span[contains(normalize-space(), 'Add another Room')]]")
                driver.execute_script("arguments[0].click();", addAnotherRoom)            
                time.sleep(2)
            
            fill_dropdown(driver,f'(//mat-select[@id="PropertyRooms[].RoomLevel"])[{roomNumber}]',Listings_Dict,"DraftRoomsDetail_RoomLevel_"+str(roomNumber),exceptionDict,logger,searchMode=True,useXpath=True)

            fill_dropdown(driver,f'(//mat-select[@id="PropertyRooms[].RoomType"])[{roomNumber}]',Listings_Dict,"DraftRoomsDetail_RoomType_"+str(roomNumber),exceptionDict,logger,searchMode=True,useXpath=True)

            fill_textbox(driver,f'(//input[@id="PropertyRooms[].RoomLengthCm"])[{roomNumber}]',Listings_Dict,"DraftRoomsDetail_LengthMetres_"+str(roomNumber),exceptionDict,logger,useXpath=True)
            fill_textbox(driver,f'(//input[@id="PropertyRooms[].RoomLengthIn"])[{roomNumber}]',Listings_Dict,"DraftRoomsDetail_LengthFtIn_"+str(roomNumber),exceptionDict,logger,useXpath=True)

            fill_textbox(driver,f'(//input[@id="PropertyRooms[].RoomWidthCm"])[{roomNumber}]',Listings_Dict,"DraftRoomsDetail_WidthMetres_"+str(roomNumber),exceptionDict,logger,useXpath=True)
            fill_textbox(driver,f'(//input[@id="PropertyRooms[].RoomWidthIn"])[{roomNumber}]',Listings_Dict,"DraftRoomsDetail_WidthFtIn_"+str(roomNumber),exceptionDict,logger,useXpath=True)

            fill_textbox(driver,f'(//input[@id="PropertyRooms[].RoomHeightCm"])[{roomNumber}]',Listings_Dict,"DraftRoomsDetail_HeightMetres_"+str(roomNumber),exceptionDict,logger,useXpath=True)
            fill_textbox(driver,f'(//input[@id="PropertyRooms[].RoomHeightIn"])[{roomNumber}]',Listings_Dict,"DraftRoomsDetail_HeightFtIn_"+str(roomNumber),exceptionDict,logger,useXpath=True)

            fill_dropdown(driver,f'(//mat-select[@id="PropertyRooms[].RoomFeature1"])[{roomNumber}]',Listings_Dict,"DraftRoomsDetail_Description1_"+str(roomNumber),exceptionDict,logger,searchMode=True,useXpath=True)

            fill_dropdown(driver,f'(//mat-select[@id="PropertyRooms[].RoomFeature2"])[{roomNumber}]',Listings_Dict,"DraftRoomsDetail_Description2_"+str(roomNumber),exceptionDict,logger,searchMode=True,useXpath=True)

            fill_dropdown(driver,f'(//mat-select[@id="PropertyRooms[].RoomFeature3"])[{roomNumber}]',Listings_Dict,"DraftRoomsDetail_Description3_"+str(roomNumber),exceptionDict,logger,searchMode=True,useXpath=True)
        
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
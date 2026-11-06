import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from screens.trebb_addlisting import add_listing_page
from screens.trebb_loginpage import login_page
from screens.trebb_draftlocation import draft_location_page
from screens.trebb_draftamountsdates import draft_amountsdates_page
from screens.trebb_draftexterior import draft_exterior_page
from screens.trebb_draftwaterfrontrural import draft_waterfrontrural_page
from screens.trebb_draftinterior import draft_interior_page
from screens.trebb_draftroomsdetail import draft_roomsdetail_page
from screens.trebb_draftcomments import draft_comments_page
from screens.trebb_draftother import draft_other_page
from screens.trebb_draftphotos import draft_photos_page
from screens.trebb_draftattachments import draft_attachments_page
from screens.trebb_draftpublicopenhouse import draft_publicopenhouse_page
from screens.trebb_draftfinancialinformation import draft_financialinformation_page
from screens.trebb_draftdetails import draft_details_page
from screens.trebb_allfunctions import get_traceback

def trebb_main(recordId,existingListingFlag,driver,Listings_Dict,trebbUrl,trebbUsername,trebbPassword,exceptionDict,logger):
    try:
        property_class = Listings_Dict["AddListing_PropertyClass"]
        transaction_type = Listings_Dict["AddListing_TransactionType"]

        Listings_Dict["Is_Freehold"] = property_class == "Residential Freehold"
        Listings_Dict["Is_Condo"] = property_class == "Residential Condo & Other"
        Listings_Dict["Is_Commercial"] = property_class == "Commercial"

        Listings_Dict["Is_ForSale"] = transaction_type == "For Sale"
        Listings_Dict["Is_ForLease"] = transaction_type == "For Lease"
        Listings_Dict["Is_ForSublease"] = transaction_type == "For Sub-Lease"

        time.sleep(5)
        login_page(driver,trebbUrl,trebbUsername,trebbPassword,exceptionDict,logger)
        time.sleep(1)
        addOrEditListingButton=driver.find_element(By.XPATH,"//div[@class='tools__name' and text()='Add/Edit Listing']")
        driver.execute_script("arguments[0].click();", addOrEditListingButton)
        time.sleep(2)
        WebDriverWait(driver, 60).until(lambda d: len(d.window_handles) == 2)
        driver.switch_to.window(driver.window_handles[1])
        if existingListingFlag:
            draftsTabButton=driver.find_element(By.XPATH, "//div[@role='tab' and .//span[normalize-space()='Drafts']]")
            driver.execute_script("arguments[0].click();", draftsTabButton)
            time.sleep(5)
    
            searchDrafts=driver.find_element(By.XPATH, "//input[@placeholder='Search by MLS#, Address, or Agent Full Name']")
            searchDrafts.clear()
            searchDrafts.send_keys(Listings_Dict["AddListing_Address"])
            time.sleep(5)
    
            rows = driver.find_elements(By.XPATH, "//tr[@role='row' and starts-with(@id, 'draftsDraft')]")
            expectedAddress = " ".join(Listings_Dict.get("AddListing_Address", "").lower().split())
            expectedCity = " ".join(Listings_Dict.get("AddListing_Municipality", "").lower().split())
            expectedPostal = " ".join(Listings_Dict.get("AddListing_PostalCode", "").lower().split())
            matched_row = None
            for row in rows:
                address_cell = row.find_element(By.XPATH, ".//td[contains(@class, 'cdk-column-streetNumber')]")
                actual_address = " ".join(address_cell.text.lower().split())
                if (expectedAddress in actual_address and expectedCity in actual_address and expectedPostal in actual_address):
                    matched_row = row
                    break
            if matched_row:
                driver.execute_script("arguments[0].click();", matched_row)
                time.sleep(3)
            else:
                addListingButton=driver.find_element(By.XPATH, "//div[@role='tab' and .//span[normalize-space()='Add Listing']]")
                driver.execute_script("arguments[0].click();", addListingButton)
                time.sleep(5)
                add_listing_page(driver, Listings_Dict, exceptionDict, logger)
                time.sleep(2)
        else:
            add_listing_page(driver, Listings_Dict, exceptionDict, logger)
            time.sleep(2)

        draft_location_page(driver, Listings_Dict, exceptionDict, logger)

        draft_amountsdates_page(driver, Listings_Dict, exceptionDict, logger)

        if Listings_Dict["Is_Freehold"] or Listings_Dict["Is_Condo"]:
            draft_exterior_page(driver, Listings_Dict, exceptionDict, logger)

            draft_waterfrontrural_page(driver, Listings_Dict, exceptionDict, logger)

            draft_interior_page(driver, Listings_Dict, exceptionDict, logger)

            draft_roomsdetail_page(driver, Listings_Dict, exceptionDict, logger)
        else:
            draft_details_page(driver, Listings_Dict, exceptionDict, logger)

        draft_comments_page(driver, Listings_Dict, exceptionDict, logger)

        if Listings_Dict["Is_Commercial"]:
            draft_financialinformation_page(driver, Listings_Dict, exceptionDict, logger)

        draft_other_page(driver, Listings_Dict, exceptionDict, logger)

        draft_photos_page(driver, Listings_Dict, exceptionDict, logger)

        draft_attachments_page(driver, Listings_Dict, exceptionDict, logger)

        draft_publicopenhouse_page(driver, Listings_Dict, exceptionDict, logger)

        case_notes = f"All screens completed successfully for record {recordId}: "
        return case_notes
    except Exception as e:
        logger.error(e)
        exceptionDict["Status"]="Failed"
        if exceptionDict["Exception type"]=="":
            exceptionDict["Exception type"]="Application"
        if exceptionDict["Exception Message"]=="":
            exceptionDict["Exception Message"]=get_traceback(e)
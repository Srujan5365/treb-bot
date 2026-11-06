import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from selenium.webdriver.common.keys import Keys
from screens.trebb_allfunctions import get_traceback, check_exceptiondict,fill_dropdown,fill_textbox,fill_yesnobutton,fill_combobox,check_ui_errors


def draft_amountsdates_page(driver, Listings_Dict, exceptionDict, logger):
    try:

        #fill_dropdown(driver,"",Listings_Dict,"DraftAmountsDates_",exceptionDict,logger)
        #fill_textbox(driver,"",Listings_Dict,"DraftAmountsDates_",exceptionDict,logger)
        #fill_yesnobutton(driver,"","",Listings_Dict,"DraftAmountsDates_",exceptionDict,logger)
        #fill_combobox(driver,"",Listings_Dict,"DraftAmountsDates_",exceptionDict,logger,searchMode=True)
        
        if Listings_Dict["Is_ForSale"] or Listings_Dict["Is_Commercial"]:
            fill_textbox(driver,"TaxAssessedValue",Listings_Dict,"DraftAmountsDates_Assessment",exceptionDict,logger)
            fill_dropdown(driver,"AssessmentYear",Listings_Dict,"DraftAmountsDates_AssessmentYear",exceptionDict,logger)
        
        fill_textbox(driver,"ListingContractDate",Listings_Dict,"DraftAmountsDates_ContractCommencement",exceptionDict,logger)
        
        fill_textbox(driver,"ExpirationDate",Listings_Dict,"DraftAmountsDates_ExpiryDate",exceptionDict,logger)

        fill_textbox(driver,"HoldoverDays",Listings_Dict,"DraftAmountsDates_HoldoverDays",exceptionDict,logger)

        if Listings_Dict["Is_ForSale"] and Listings_Dict["Is_Condo"]:
            fill_textbox(driver,"NumberSharesPercent",Listings_Dict,"DraftAmountsDates_SharesPercent",exceptionDict,logger)

        
        
        fill_yesnobutton(driver,"LandLeaseYN-true-button","LandLeaseYN-false-button",Listings_Dict,"DraftAmountsDates_LandLease",exceptionDict,logger)
        
        fill_textbox(driver,"LeasedLandFee",Listings_Dict,"DraftAmountsDates_LeasedLandFee",exceptionDict,logger)

        fill_dropdown(driver,"LandLeaseAmountFrequency",Listings_Dict,"DraftAmountsDates_LandLeaseAmountFrequency",exceptionDict,logger)

        fill_textbox(driver,"LandLeaseExpirationDate",Listings_Dict,"DraftAmountsDates_LandLeaseExpirationDate",exceptionDict,logger)
        
        fill_yesnobutton(driver,"LocalImprovements-true-button","LocalImprovements-false-button",Listings_Dict,"DraftAmountsDates_LocalImprovements",exceptionDict,logger)
        
        fill_textbox(driver,"LocalImprovementsComments",Listings_Dict,"DraftAmountsDates_LocalImprovementsComments",exceptionDict,logger)

        fill_textbox(driver,"PhasedInTaxAssessedValue",Listings_Dict,"DraftAmountsDates_PhasedInTaxAssessedValue",exceptionDict,logger)

        fill_textbox(driver,"PossessionDate",Listings_Dict,"DraftAmountsDates_PossessionDate",exceptionDict,logger)
        
        fill_textbox(driver,"PossessionDetails",Listings_Dict,"DraftAmountsDates_PossessionRemarks",exceptionDict,logger)

        fill_dropdown(driver,"PossessionType",Listings_Dict,"DraftAmountsDates_PossessionType",exceptionDict,logger)
        
        fill_textbox(driver,"RoadAccessFee",Listings_Dict,"DraftAmountsDates_RoadAccessFee",exceptionDict,logger)
        
        if Listings_Dict["Is_Condo"]:
            fill_textbox(driver,"AssociationFee",Listings_Dict,"DraftAmountsDates_Maintenance",exceptionDict,logger)
                
        
        if Listings_Dict["Is_ForSale"]:
            fill_yesnobutton(driver,"AdjustedHSTRebateYN-true-button","AdjustedHSTRebateYN-false-button",Listings_Dict,"DraftAmountsDates_ListPriceToReducedReflectHSTRebate",exceptionDict,logger)
            
            fill_combobox(driver,"HSTApplication",Listings_Dict,"DraftAmountsDates_HSTApplicableToSamePrice",exceptionDict,logger)
            
            fill_combobox(driver,"DevelopmentChargesPaid",Listings_Dict,"DraftAmountsDates_DevelopmentChargesPaid",exceptionDict,logger)

        
        if Listings_Dict["Is_ForSale"] or Listings_Dict["Is_Commercial"]:
            fill_dropdown(driver,"TaxType",Listings_Dict,"DraftAmountsDates_TaxType",exceptionDict,logger)
                        
            fill_dropdown(driver,"TaxYear",Listings_Dict,"DraftAmountsDates_TaxYear",exceptionDict,logger)
            fill_textbox(driver,"TaxAnnualAmount",Listings_Dict,"DraftAmountsDates_Taxes",exceptionDict,logger)
            
        fill_textbox(driver,"OwnerName",Listings_Dict,"DraftAmountsDates_LandlordName",exceptionDict,logger)

            
        fill_textbox(driver,"ListPrice",Listings_Dict,"DraftAmountsDates_ListPrice",exceptionDict,logger)

        if Listings_Dict["Is_Commercial"] or (Listings_Dict["Is_ForSale"] and Listings_Dict["Is_Condo"]):
            fill_textbox(driver,"MinimumRentalTermMonths",Listings_Dict,"DraftAmountsDates_MinimumRentalTermMonths",exceptionDict,logger)

            fill_textbox(driver,"MaximumRentalMonthsTerm",Listings_Dict,"DraftAmountsDates_MaximumRentalMonthsTerm",exceptionDict,logger)

            fill_dropdown(driver,"ListPriceUnit",Listings_Dict,"DraftAmountsDates_ListPriceCode",exceptionDict,logger)

        if Listings_Dict["Is_Commercial"]:    
            fill_textbox(driver,"CommercialCondoFee",Listings_Dict,"DraftAmountsDates_CommercialCondoFeeMonthly",exceptionDict,logger)

        if Listings_Dict["Is_ForSale"] or Listings_Dict["Is_Commercial"]:   
            fill_textbox(driver,"MortgageComment",Listings_Dict,"DraftAmountsDates_MortgageComments",exceptionDict,logger)

                        
        if not Listings_Dict["Is_ForSale"] and not Listings_Dict["Is_Commercial"]:
            fill_dropdown(driver,"PaymentFrequency",Listings_Dict,"DraftAmountsDates_PaymentFrequency",exceptionDict,logger)

            fill_dropdown(driver,"PaymentMethod",Listings_Dict,"DraftAmountsDates_PaymentMethod",exceptionDict,logger)
                        
            fill_dropdown(driver,"LeaseTerm",Listings_Dict,"DraftAmountsDates_LeaseTerm",exceptionDict,logger)
            fill_yesnobutton(driver,"RentalApplicationYN-true-button","RentalApplicationYN-false-button",Listings_Dict,"DraftAmountsDates_RentalApplicationRequired",exceptionDict,logger)
                        
            fill_yesnobutton(driver,"DepositRequired-true-button","DepositRequired-false-button",Listings_Dict,"DraftAmountsDates_DepositRequired",exceptionDict,logger)
            fill_yesnobutton(driver,"LeaseAgreementYN-true-button","LeaseAgreementYN-false-button",Listings_Dict,"DraftAmountsDates_LeaseAgreement",exceptionDict,logger)
            fill_yesnobutton(driver,"ReferencesRequiredYN-true-button","ReferencesRequiredYN-false-button",Listings_Dict,"DraftAmountsDates_ReferencesRequired",exceptionDict,logger)
                                              
            fill_yesnobutton(driver,"CreditCheckYN-true-button","CreditCheckYN-false-button",Listings_Dict,"DraftAmountsDates_CreditCheck",exceptionDict,logger)
            fill_yesnobutton(driver,"EmploymentLetterYN-true-button","EmploymentLetterYN-false-button",Listings_Dict,"DraftAmountsDates_EmploymentLetter",exceptionDict,logger)
            fill_yesnobutton(driver,"NonSmokingPolicy-true-button","NonSmokingPolicy-false-button",Listings_Dict,"DraftAmountsDates_NonSmokingPolicy",exceptionDict,logger)
                                          
            fill_yesnobutton(driver,"BuyOptionYN-true-button","BuyOptionYN-false-button",Listings_Dict,"DraftAmountsDates_BuyOption",exceptionDict,logger)
        
            fill_combobox(driver,"RentIncludes",Listings_Dict,"DraftAmountsDates_IncludedInLeaseCost",exceptionDict,logger,searchMode=True,expandButtonName="Included in Lease Cost")
        
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
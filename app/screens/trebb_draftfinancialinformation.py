import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from selenium.webdriver.common.keys import Keys
from screens.trebb_allfunctions import get_traceback, check_exceptiondict,fill_dropdown,fill_textbox,fill_yesnobutton,fill_combobox,check_ui_errors


def draft_financialinformation_page(driver, Listings_Dict, exceptionDict, logger):
    try:
        #fill_dropdown(driver,"",Listings_Dict,"DraftAmountsDates_",exceptionDict,logger)
        #fill_textbox(driver,"",Listings_Dict,"DraftAmountsDates_",exceptionDict,logger)
        #fill_yesnobutton(driver,"","",Listings_Dict,"DraftAmountsDates_",exceptionDict,logger)
        #fill_combobox(driver,"",Listings_Dict,"DraftAmountsDates_",exceptionDict,logger,searchMode=True)
        
        fill_yesnobutton(driver,"FinancialStatementAvailableYN-true-button","FinancialStatementAvailableYN-false-button",Listings_Dict,"DraftFinancialInformation_FinancialStatement",exceptionDict,logger)

        fill_yesnobutton(driver,"ChattelsYN-true-button","ChattelsYN-false-button",Listings_Dict,"DraftFinancialInformation_Chattels",exceptionDict,logger)

        fill_yesnobutton(driver,"FranchiseYN-true-button","FranchiseYN-false-button",Listings_Dict,"DraftFinancialInformation_Franchise",exceptionDict,logger)

        fill_dropdown(driver,"HoursDaysOfOperation",Listings_Dict,"DraftFinancialInformation_DaysOpen",exceptionDict,logger)

        fill_textbox(driver,"HoursDaysOfOperationDescription",Listings_Dict,"DraftFinancialInformation_HoursOpen",exceptionDict,logger)

        fill_textbox(driver,"NumberOfFullTimeEmployees",Listings_Dict,"DraftFinancialInformation_Employees",exceptionDict,logger)

        fill_textbox(driver,"SeatingCapacity",Listings_Dict,"DraftFinancialInformation_Seats",exceptionDict,logger)

        fill_yesnobutton(driver,"LiquorLicenseYN-true-button","LiquorLicenseYN-false-button",Listings_Dict,"DraftFinancialInformation_LLBO",exceptionDict,logger)

        fill_textbox(driver,"BusinessName",Listings_Dict,"DraftFinancialInformation_BusinessBuildingName",exceptionDict,logger)

        fill_textbox(driver,"TaxesExpense",Listings_Dict,"DraftFinancialInformation_TaxesExpense",exceptionDict,logger)

        fill_textbox(driver,"InsuranceExpense",Listings_Dict,"DraftFinancialInformation_InsuranceExpense",exceptionDict,logger)

        fill_textbox(driver,"ProfessionalManagementExpense",Listings_Dict,"DraftFinancialInformation_ManagementExpense",exceptionDict,logger)

        fill_textbox(driver,"MaintenanceExpense",Listings_Dict,"DraftFinancialInformation_MaintenanceExpense",exceptionDict,logger)

        fill_textbox(driver,"HeatingExpenses",Listings_Dict,"DraftFinancialInformation_HeatExpenses",exceptionDict,logger)

        fill_textbox(driver,"ElectricExpense",Listings_Dict,"DraftFinancialInformation_HydroExpense",exceptionDict,logger)

        fill_textbox(driver,"WaterExpense",Listings_Dict,"DraftFinancialInformation_WaterExpense",exceptionDict,logger)

        fill_textbox(driver,"OtherExpense",Listings_Dict,"DraftFinancialInformation_OtherExpense",exceptionDict,logger)

        fill_textbox(driver,"GrossRevenue",Listings_Dict,"DraftFinancialInformation_GrossIncomeSales",exceptionDict,logger)

        fill_textbox(driver,"VacancyAllowance",Listings_Dict,"DraftFinancialInformation_VacancyAllowance",exceptionDict,logger)

        fill_textbox(driver,"OperatingExpense",Listings_Dict,"DraftFinancialInformation_OperatingExpense",exceptionDict,logger)

        fill_textbox(driver,"NetOperatingIncome",Listings_Dict,"DraftFinancialInformation_NetIncomeBeforeDebt",exceptionDict,logger)

        fill_textbox(driver,"EstimatedInventoryValueAtCost",Listings_Dict,"DraftFinancialInformation_EstimatedInventoryValueAtCost",exceptionDict,logger)

        fill_textbox(driver,"CommonAreaUpcharge",Listings_Dict,"DraftFinancialInformation_CommonAreaUpcharge",exceptionDict,logger)

        fill_textbox(driver,"PercentRent",Listings_Dict,"DraftFinancialInformation_PercentageRent",exceptionDict,logger)

        fill_dropdown(driver,"Expenses",Listings_Dict,"DraftFinancialInformation_ExpensesActualEstimated",exceptionDict,logger)

        fill_textbox(driver,"YearExpenses",Listings_Dict,"DraftFinancialInformation_YearExpenses",exceptionDict,logger)
        
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
    
    
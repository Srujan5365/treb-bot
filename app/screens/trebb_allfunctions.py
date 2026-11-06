import sys,traceback,time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys


OVERLAY = "//div[contains(@class,'cdk-overlay-pane')]"
def get_traceback(e):
    """
    Extracts the deepest file name and line number from the current exception
    and returns a beautifully formatted dictionary.
    """
    # 1. Extract execution details
    exc_type, exc_obj, exc_tb = sys.exc_info()
    
    # Check if a traceback object actually exists to prevent an IndexError
    if exc_tb is not None:
        tb_frame = traceback.extract_tb(exc_tb)[-1]
        filename = tb_frame.filename
        line_number = tb_frame.lineno
    else:
        filename = "Unknown File"
        line_number = "Unknown Line"
        
    # 2. Build and return the structured dictionary
    return f" Error: {e} | File: {filename} | Line: {line_number}"


def check_exceptiondict(exceptionDict):
    if exceptionDict=={"Status":"","Exception type":"","Exception Message":""}:
        return True
    return False

def fill_textbox(driver,htmlIDOrXpath,Listings_Dict,keyNameInDict,exceptionDict,logger,checkMode=False,useXpath=False):
    try:
        runMode=True
        if Listings_Dict.get(keyNameInDict,""):
            if useXpath:
                textboxInUI=driver.find_element(By.XPATH, htmlIDOrXpath)
            else:
                textboxInUI=driver.find_element(By.ID, htmlIDOrXpath)
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", textboxInUI)
            if checkMode:
                try:
                    current_value = " ".join(textboxInUI.text.lower().split())
                except Exception:
                    current_value = ""
                expected_value = " ".join(str(Listings_Dict[keyNameInDict]).lower().split())
                if current_value == expected_value:
                    runMode = False
            if runMode:
                textboxInUI.clear()
                time.sleep(1)
                textboxInUI.send_keys(Listings_Dict[keyNameInDict])
                time.sleep(1)
        else:
            logger.info(f"HTML ID - {htmlIDOrXpath} with Key Name - {keyNameInDict} is Non Mandatory Field")
    except Exception as e:
        logger.error(e)
        if check_exceptiondict(exceptionDict):
            exceptionDict["Status"] = "Failed"
            exceptionDict["Exception type"] = "Application"
            exceptionDict["Exception Message"] = get_traceback(e)
        raise

def fill_dropdown(driver,htmlIDOrXpath,Listings_Dict,keyNameInDict,exceptionDict,logger,searchMode=False,checkMode=False,useXpath=False):
    try:
        runMode=True
        if Listings_Dict.get(keyNameInDict,""):
            if useXpath:
                dropdownInUI=driver.find_element(By.XPATH, htmlIDOrXpath)
            else:
                dropdownInUI=driver.find_element(By.ID, htmlIDOrXpath)
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dropdownInUI)
            if checkMode:
                try:
                    current_value = " ".join(dropdownInUI.text.lower().split())
                except Exception:
                    current_value = ""
                expected_value = " ".join(str(Listings_Dict[keyNameInDict]).lower().split())
                if current_value == expected_value:
                    runMode = False
            if runMode:
                driver.execute_script("arguments[0].click();", dropdownInUI)
                time.sleep(1)
                if searchMode:
                    driver.find_element(By.XPATH, OVERLAY + "//input[@aria-label='Search']").clear()
                    driver.find_element(By.XPATH, OVERLAY + "//input[@aria-label='Search']").send_keys(Listings_Dict[keyNameInDict])
                    time.sleep(1)
                dropdownInUIOption = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, OVERLAY + f"//mat-option[contains(normalize-space(.),'{Listings_Dict[keyNameInDict]}')]")))
                driver.execute_script("arguments[0].click();", dropdownInUIOption)
                time.sleep(1)
        else:
            logger.info(f"HTML ID - {htmlIDOrXpath} with Key Name - {keyNameInDict} is Non Mandatory Field")
    except Exception as e:
        logger.error(e)
        if check_exceptiondict(exceptionDict):
            exceptionDict["Status"] = "Failed"
            exceptionDict["Exception type"] = "Application"
            exceptionDict["Exception Message"] = get_traceback(e)
        raise

def fill_yesnobutton(driver,htmlYesID,htmlNoID,Listings_Dict,keyNameInDict,exceptionDict,logger):
    try:
        if Listings_Dict.get(keyNameInDict,"")=="Yes":
            UIYesButton=driver.find_element(By.ID, htmlYesID)
            if not UIYesButton.is_selected():
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",UIYesButton)
                driver.execute_script("arguments[0].click();", UIYesButton)
        elif Listings_Dict.get(keyNameInDict,"")=="No":
            UINoButton=driver.find_element(By.ID, htmlNoID)
            if not UINoButton.is_selected():
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",UINoButton)
                driver.execute_script("arguments[0].click();", UINoButton)
        else:
            logger.info(f"HTML ID - {htmlYesID} with Key Name - {keyNameInDict} is Non Mandatory Field")
        time.sleep(1)

    except Exception as e:
        logger.error(e)
        if check_exceptiondict(exceptionDict):
            exceptionDict["Status"] = "Failed"
            exceptionDict["Exception type"] = "Application"
            exceptionDict["Exception Message"] = get_traceback(e)
        raise



def fill_combobox(driver,htmlID,Listings_Dict,keyNameInDict,exceptionDict,logger,searchMode=False,expandButtonName=None):
    try:
        if Listings_Dict.get(keyNameInDict,""):
            comboboxInUI=driver.find_element(By.ID,htmlID)
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", comboboxInUI)
            if searchMode and expandButtonName:
                expandButton=comboboxInUI.find_element(By.XPATH,f'.//button[normalize-space(.)="{expandButtonName}"]')
                driver.execute_script("arguments[0].click();",expandButton)
                time.sleep(1)
            for option in Listings_Dict[keyNameInDict].split(","):
                option=option.strip()
                selectedOption=comboboxInUI.find_elements(By.XPATH,f'.//button[@role="option"][normalize-space(.)="{option}"]')
                if any(el.get_attribute("aria-selected")=="true" for el in selectedOption):
                    continue
                if searchMode:
                    searchInput=WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,OVERLAY+"//input[@aria-label='Search']")))
                    searchInput.clear()
                    searchInput.send_keys(option)
                    time.sleep(1)
                    optionToBeSelected=driver.find_elements(By.XPATH,OVERLAY+f'//button[@role="option"][normalize-space(.)="{option}"]')
                else:
                    optionToBeSelected=selectedOption
                if optionToBeSelected:
                    optionElement=optionToBeSelected[0]
                    if optionElement.get_attribute("aria-selected")!="true":
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", optionElement)
                        driver.execute_script("arguments[0].click();",optionElement)
                        time.sleep(1)
                else:
                    raise Exception(f"HTML ID - {htmlID} with Key Name - {keyNameInDict} does not contain '{option}' as an available option on UI to select")
            if searchMode and expandButtonName:
                try:
                    driver.execute_script("arguments[0].click();",expandButton)
                    time.sleep(1)
                except:
                    pass
        else:
            logger.info(f"HTML ID - {htmlID} with Key Name - {keyNameInDict} is Non Mandatory Field")
    except Exception as e:
        logger.error(e)
        if check_exceptiondict(exceptionDict):
            exceptionDict["Status"]="Failed"
            exceptionDict["Exception type"]="Application"
            exceptionDict["Exception Message"]=get_traceback(e)
        raise


def check_ui_errors(driver):
    errors = driver.find_elements(By.CSS_SELECTOR, "mat-error")
    error_messages = [error.text.strip() for error in errors if error.is_displayed() and error.text.strip()]
    if error_messages:
        raise Exception("UI Validation Failed: " + " | ".join(error_messages))

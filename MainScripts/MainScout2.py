#START SCRIPT




#---------------------------------------------------------------------------------------------------------------------------------------------------



#START IMPORTING LIBRARIES
#===================================================================================================================================================
    #MAINSCRIPTS
from MainScout1 import *
    #SELENIUM
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
    #TIME
import time
import datetime
    #JSON
import json
    #MULTIPROCESSING
import multiprocessing
from functools import partial
#===================================================================================================================================================
#END IMPORTING LIBRARIES 



#---------------------------------------------------------------------------------------------------------------------------------------------------



#FUNCTION CREATION START
#===================================================================================================================================================
    #SELENIUM/BROWSER DRIVER SETUP // RETURN BROWSER DRIVER // FUNCTION
def selenium_setup():
        #DEFINE CHROME CAPABILITIES TO WAIT FOR PAGE TO BE INTERACTIVE INSTEAD OF FULL LOAD
    chrome_capabilities = DesiredCapabilities().CHROME
    chrome_capabilities["pageLoadStrategy"] = "eager"
        #DEFINE CHROME OPTIONS
    chrome_options = webdriver.ChromeOptions()
    user_agent ='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_options.add_argument("--lang=en-US,en;q=.9")
    chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--incognito")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation']) 
    chrome_options.add_experimental_option('useAutomationExtension', False)
        #SET SELENIUM CHROME DRIVER CAPABILITIES/OPTIONS/PATH HERE
    browser_driver = webdriver.Chrome(desired_capabilities=chrome_capabilities, options=chrome_options, executable_path=r'C:\Users\Mason\Desktop\DeliverMeScraper\chromedriver.exe')
        #RETURN BROWSER
    return browser_driver
#===================================================================================================================================================
    #RUN SELENIUM/BROWSER // RETURN SELENIUM SESSION COOKIES // FUNCTION
def run_selenium_browser(current_zip_code, current_city, browser_driver, url):
    #proxy.new_har("peapod")
        #LOAD PEAPOD
    browser_driver.get(url)
        #FIND INITIAL ZIP CODE ELEMENTS
    zip_entry = browser_driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div/main/div/div/section[3]/div[2]/zipcode-entry/div/form/div[2]/div/label/div[1]/input')
    submit_button = browser_driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div/main/div/div/section[3]/div[2]/zipcode-entry/div/form/div[2]/div/label/div[2]/button')
        #SEND INITIAL ZIP CODE INPUTS
    zip_entry.send_keys(current_zip_code)
    submit_button.click()
        #PAUSE FOR .5 SECONDS TO ENSURE OPTIONS FOR CITIES LOAD
    time.sleep(.5)
        #CHECK FOR CITIES INPUT
    try:
            #CLICK CITY DROP DOWN FOR CITY OPTIONS
        cities_entry_first_click = browser_driver.find_element_by_css_selector('#main-content > div > section.gateway-page_body-content-wrapper.gateway-page_body-content-wrapper--no-margin > div.gateway-body-content_login-wrapper.gateway-body-content_login-wrapper--rounded-corners > zipcode-entry > div > form > div.gateway-login_single-field-wrapper > div.trailer--double > label > div > div.select-field > select')
        cities_entry_first_click.click()
            #CYCLE THROUGH DROP DOWN MENU CITY OPTIONS FOR CORRECT CITY
        for cities_entry_second_click in cities_entry_first_click.find_elements_by_tag_name('option'):
            if current_city in cities_entry_second_click.text:
                cities_entry_second_click.click()
                break
            #CLICK SUBMIT TO SEND CITY SELECTION
        cities_entry_third_click = browser_driver.find_element_by_css_selector('#main-content > div > section.gateway-page_body-content-wrapper.gateway-page_body-content-wrapper--no-margin > div.gateway-body-content_login-wrapper.gateway-body-content_login-wrapper--rounded-corners > zipcode-entry > div > form > div.gateway-login_single-field-wrapper > div.button-container > div.button-container_control.button-container_control--no-outer-spacing.omega > button')
        cities_entry_third_click.click() 
    except:
        pass
        #GRAB SELENIUM SESSION COOKIES / PAUSE FOR .5 SECONDS TO ENSURE GUEST COOKIES LOAD 
    time.sleep(.5)
    selenium_cookies = browser_driver.get_cookies()
        #QUIT SELENIUM BROWSER / RETURN SELENIUM COOKIES
    #print(proxy.har)
    #server.stop()
    browser_driver.quit()
    return selenium_cookies
#===================================================================================================================================================
    #RUN AUTOMATED SELENIUM BROWSER TO GET GUEST SESSION COOKIES // RETURNS SELENIUM SESSION COOKIES // FUNCTION
def get_selenium_cookies(Account_Database):
        #CORRECTLY TRANSLATE/UNPACK MULTOPROCESSING ITERATED ACCOUNT DATABSE
    if (Account_Database[0].isdigit() == True):
        current_zip_code = Account_Database[0]
        current_city = Account_Database[1]
    else:
        current_zip_code = Account_Database[1]
        current_city = Account_Database[0]
        #DEFINE TARGET URL
    url = 'https://www.peapod.com'
        #EXECUTE BROWSER SETUP
    browser_driver = selenium_setup()    
        #EXECUTE SELENIUM BROWSER
    selenium_cookies = run_selenium_browser(current_zip_code, current_city, browser_driver, url)
        #RETURN SELENIUM COOKIES
    return selenium_cookies
#===================================================================================================================================================
    #RUN AUTO BROWSER //// GET ACCOUNT INFO TO CHECK FOR AVAILABILITY -> OPEN BROWSER AND INPUT DATA TO CREATE GUEST SESSION COOKIES -> RETURN SELENIUM GUEST SESSION SELENIUM COOKIES //// FUNCTION
def run_auto_browser(Account_Database):
    start_time = time.time()
    print("")
        #RUN PARALLEL PROCESS FOR EACH UNIQUE ZIP/CITY COMBO AND STORE SELENIUM COOKIES
    with multiprocessing.Pool(processes=len(Account_Database)) as pool:
        all_selenium_guest_session_cookies = pool.map(get_selenium_cookies, Account_Database)
    end_time = time.time()
    print("Selenium runtime: " + str(end_time - start_time))
        #RETURN ALL SELENIUM GUEST SESSION COOKIES
    return all_selenium_guest_session_cookies
#===================================================================================================================================================
    #MAIN EXECUTION // EXECUTE MAIN FUNCTION // FUNCTION
def MainScout2():
    all_selenium_guest_session_cookies = run_auto_browser(create_Account_Database_Array_Function(number_Of_Accounts_Function()))
    return all_selenium_guest_session_cookies
#===================================================================================================================================================
#FUNCTION CREATION END



#---------------------------------------------------------------------------------------------------------------------------------------------------



#FUNCTION EXECUTION START
#===================================================================================================================================================
#if __name__ == '__main__':
    #MainScout2()
#===================================================================================================================================================
#FUNCTION EXECUTION END



#---------------------------------------------------------------------------------------------------------------------------------------------------




#END SCRIPT
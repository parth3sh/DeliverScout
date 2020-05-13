#START SCRIPT




#---------------------------------------------------------------------------------------------------------------------------------------------------



#START IMPORTING LIBRARIES
#===================================================================================================================================================
    #SELENIUM
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
    #BEAUTIFUL SOUP
from bs4 import BeautifulSoup
    #REQUESTS
import requests
    #JSON
import json
    #TIME
import time
import datetime
from datetime import date 
from datetime import timedelta 
    #MULTIPROCESSING
import multiprocessing
from functools import partial
#===================================================================================================================================================
#END IMPORTING LIBRARIES 



#---------------------------------------------------------------------------------------------------------------------------------------------------



#FUNCTION CREATION START
#===================================================================================================================================================
    #HOW MANY ACCOUNTS // RETURN HOW MANY ACCOUNTS // FUNCTION
def number_Of_Accounts_Function():
    number_Of_Accounts = int(input('Input the number of accounts you have:'))
    return number_Of_Accounts
#===================================================================================================================================================
    #CREATE/INPUT USER INFO DATABASE // RETURN INFO DATABASE // FUNCTION
def create_Account_Database_Array_Function(number_Of_Accounts):
    width, height = 2, number_Of_Accounts
    account_Database_Array = [[0 for x in range(width)] for y in range(height)] 

    for x in range(number_Of_Accounts):
        user_zip_code = input('Input your zip code for account #' + str(x+1) + ':')
        user_city = input('Input your city for account #' + str(x+1) + ':')

        account_Database_Array[x][0] = user_zip_code
        account_Database_Array[x][1] = user_city

    return account_Database_Array
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
    #CREATE NEXT TWO WEEKS TO CHECK DATES DICTIONARY // RETURN DATES DICTIONARY // FUNCTION
def create_dates_inquiry_dictionary():
        #CREATE EMPTY DICTIONARY
    dates_dictionary = []
        #SKIP TODAY AND CYCLE THROUGH NEXT 13 DAYS ADDING EACH AS YEAR/MONTH/DAY FORMAT TO DICTIONARY
    for x in range(13):
        x = x+1
        today = date.today()
        today += datetime.timedelta(days=x)
        dates_dictionary.append(today)
        #RETURN FILLED DATES DICTIONARY
    return dates_dictionary
#===================================================================================================================================================
    #SEND GET REQUESTS FOR AVAILABILITY DATA // RETURN RAW JSON DATA DICTIONARY // FUNCTION
def send_get_requests(selenium_cookies, headers, today):
        #START A REQUESTS SESSION AS 'session'
    with requests.Session() as session:
            #SETUP REQUESTS / PASS SELENIUM COOKIES TO REQUESTS SESSION
        for cookie in selenium_cookies:
            session.cookies.set(cookie['name'], cookie['value'])
            #DEFINE EMPTY RAW DATA DICTIONARY
        raw_data_dictionary = []
            #DEFINE API URL WHERE SLOT AVAILABILITY IS STORED / GET REQUEST PARAMETERS
        availability_url = 'https://www.peapod.com/api/v2.0/user/slots'
        params = {
            'delivAvail': 'true',
            'headers': 'true',
            'pupAvail': 'true',
            'selected': 'true',
            'serviceType': 'D',
            'viewDate': today
        }
            #SEND GET REQUEST / STORE FULL SERVER GET RESPONSE
        availability_response = session.get(availability_url, headers = headers, params= params)
            #PULL RAW JSON DATA FROM RESPONSE
        availability_json = availability_response.json()
            #APPEND RAW JSON DATA TO RAW DATA DICTIONARY
        raw_data_dictionary.append(availability_json)
            #END REQUESTS SESSION / RETURN RAW DATA DICTIONARY
        session.close()   
        return raw_data_dictionary
#===================================================================================================================================================
    #RUN AUTOMATED SELENIUM BROWSER TO GET GUEST SESSION COOKIES // RETURNS SELENIUM SESSION COOKIES // FUNCTION
def get_selenium_cookies(current_zip_code, current_city):
        #DEFINE TARGET URL
    url = 'https://www.peapod.com'
        #EXECUTE BROWSER SETUP
    browser_driver = selenium_setup()    
        #EXECUTE SELENIUM BROWSER
    selenium_cookies = run_selenium_browser(current_zip_code, current_city, browser_driver, url)
        #RETURN SELENIUM COOKIES
    return selenium_cookies
#===================================================================================================================================================
    #PARSE RAW DATA DICTIONARY // RETURN AVAILABLE DATETIME JSON DATA DICTIONARY // FUNCTION
def parse_raw_json_data(raw_data_dictionary):
        #DEFINE EMPTY PARSED DATA DICTIONARY
    parsed_data_dictionary = []
        #TRY TO PARSE EACH DATETIME SLOT IN RAW DATA
    try: 
            #FOR LOOP THROUGH EACH OVERALL DATE WITH RAW JSON DATA
        for raw_json_data_date in range(len(raw_data_dictionary)):
                #FOR LOOP THROUGH EACH TIME SLOT IN A SINGLE DATE WITH RAW JSON DATA / NOTED: ADDED INDEX '[0]' COMPENSATES FOR MULTIPROCESSING ADDING AN EXTRA DICTIONARY LAYER 
            for slot_number in raw_data_dictionary[raw_json_data_date][0]['response']['slots']:
                    #IF A SLOT IS NOT SOLD OUT THEN SAVE THE TIME START/TIME END/AND DATE
                if (slot_number['statusMsg'] != 'Sold Out'):
                    availability_date = slot_number['date']
                    availability_time_start = slot_number['timeStart'] [11:]
                    availability_time_end = slot_number['timeEnd'] [11:]
                        #CREATE CURRENT SLOT ITERATION DICTIONARY WITH TIME/DATE DATA
                    parsing_slot_availability_dictionary = [availability_date, availability_time_start, availability_time_end]
                        #APPEND OPEN TIMES/DATES TO PARSED DATA DICTIONARY
                    parsed_data_dictionary.append(parsing_slot_availability_dictionary)
    except:
        print("Error parsing raw data")
        #RETURN PARSED DATA DICTIONARY
    return parsed_data_dictionary
#===================================================================================================================================================
    #CHECK IF AVAILABLE DATETIMES EXIST IN PARSED DATA // RETURN AVAILABILITY STATUS BOOLEAN // FUNCTION
def availability_status_checker(parsed_availability_dictionary):
        #INITIAL ASSUMPTION = NO AVAILABILITY
    availability_status = False
        #CHECK AVAILABILITY WITH IF / RETURN TRUE(AVAILABLE) OR FALSE(NOT AVAILABLE)
    if not parsed_availability_dictionary:
        return availability_status
    else:
        availability_status = True
        return availability_status
#===================================================================================================================================================
    #PUSH AVAILABLE DATETIMES TO DATABASE // RETURN !!TBD!! // FUNCTION
    
#===================================================================================================================================================
    #RUN AUTO BROWSER //// GET ACCOUNT INFO TO CHECK FOR AVAILABILITY -> OPEN BROWSER AND INPUT DATA TO CREATE GUEST SESSION COOKIES -> RETURN SELENIUM GUEST SESSION SELENIUM COOKIES //// FUNCTION
def run_auto_browser(Account_Database):
        #DEFINE EMPTY SELENIUM GUEST SESSION COOKIES DICTIONARY
    all_selenium_guest_session_cookies = []
        #RUN SESSION FOR ALL EACH CODE AND CITIE
    for x in range(len(Account_Database)):
        current_zip_code = Account_Database[x][0]
        current_city = Account_Database[x][1]
            #GET CURRENT ITERATION OF AUTO BROWSER SELENIUM SESSION COOKIES
        start_time = time.time()
        selenium_cookies = get_selenium_cookies(current_zip_code, current_city)
        end_time = time.time()
        print("Selenium runtime: " + str(end_time - start_time))
            #APPEND CURRENT ITERATION OF AUTO BROWSER SELENIUM SESSION COOKIES TO DICTIONARY
        all_selenium_guest_session_cookies.append(selenium_cookies)
        #RETURN ALL SELENIUM GUEST SESSION COOKIES
    return all_selenium_guest_session_cookies
#===================================================================================================================================================
    #RUN REPEATED MULTIPROCESSING FOR SLOT DATA //// GET NEXT TWO WEEKS OF DATES DICTIOANRY -> SEND GET REQUESTS FOR RAW DATA -> PARSE RAW DATA FOR OPEN SLOTS -> PRINT AVAILABILITY -> RUN AGAIN EVERY MINUTE //// FUNCTION
def get_parse_print_raw_data (all_selenium_guest_session_cookies):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
    dates_dictionary = create_dates_inquiry_dictionary()

    x = 0
    while x < 10:
        try:
            for selenium_cookies in range(len(all_selenium_guest_session_cookies)):
                print("")
                cookies_headers_argument_wrapper = partial(send_get_requests, all_selenium_guest_session_cookies[selenium_cookies], headers)
                start_time = time.time()
                with multiprocessing.Pool(processes=13) as pool:
                    raw_data_dictionary = pool.map(cookies_headers_argument_wrapper, dates_dictionary)
                parsed_availability_dictionary = parse_raw_json_data(raw_data_dictionary)
                availability_status = availability_status_checker(parsed_availability_dictionary)
                if availability_status == True:
                    print(parsed_availability_dictionary)
                else:
                    print('No times or dates available')
                end_time = time.time()
                print("Get requests and parse data runtime: " + str(end_time - start_time))
                print("")
            print("----------------------------------------------------------------------------------------------------------------")
            time.sleep(59)
            x = x+1
        except:
            x = x+1
            print("Error: Cookie expired")
            break
#===================================================================================================================================================
#FUNCTION CREATION END



#---------------------------------------------------------------------------------------------------------------------------------------------------



#FUNCTION EXECUTION START
#===================================================================================================================================================
if __name__ == '__main__':
    all_selenium_guest_session_cookies = run_auto_browser(create_Account_Database_Array_Function(number_Of_Accounts_Function()))
    get_parse_print_raw_data(all_selenium_guest_session_cookies)
#===================================================================================================================================================
#FUNCTION EXECUTION END



#---------------------------------------------------------------------------------------------------------------------------------------------------
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
    width, height = 3, number_Of_Accounts
    account_Database_Array = [[0 for x in range(width)] for y in range(height)] 

    for x in range(number_Of_Accounts):
        user_email = input('Input your email for account #' + str(x+1) +':')
        user_zip_code = input('Input your zip code for account #' + str(x+1) + ':')
        user_city = input('Input your city for account #' + str(x+1) + ':')

        account_Database_Array[x][0] = user_email
        account_Database_Array[x][1] = user_zip_code
        account_Database_Array[x][2] = user_city

    return account_Database_Array
#===================================================================================================================================================
    #SELENIUM/BROWSER DRIVER SETUP // RETURN BROWSER DRIVER // FUNCTION
def selenium_setup():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--incognito")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation']) 
    chrome_options.add_experimental_option('useAutomationExtension', False)
        #EDIT SELENIUM DRIVER PATH HERE
    browser_driver = webdriver.Chrome(options=chrome_options, executable_path=r'C:\Users\Mason\Desktop\DeliverMeScraper\chromedriver.exe')
        #RETURN BROWSER
    return browser_driver
#===================================================================================================================================================
    #RUN SELENIUM/BROWSER // RETURN SELENIUM SESSION COOKIES // FUNCTION
def run_selenium_browser(current_zip_code, current_city, browser_driver, url):
        #LOAD PEAPOD
    browser_driver.get(url)
        #FIND INITIAL ELEMENTS
    zip_entry = browser_driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div/main/div/div/section[3]/div[2]/zipcode-entry/div/form/div[2]/div/label/div[1]/input')
    submit_button = browser_driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div/main/div/div/section[3]/div[2]/zipcode-entry/div/form/div[2]/div/label/div[2]/button')
        #SEND INITIAL INPUTS
    zip_entry.send_keys(current_zip_code)
    submit_button.click()
    time.sleep(2)
        #CHECK FOR CITIES INPUT
    try:
        cities_entry_first_click = browser_driver.find_element_by_css_selector('#main-content > div > section.gateway-page_body-content-wrapper.gateway-page_body-content-wrapper--no-margin > div.gateway-body-content_login-wrapper.gateway-body-content_login-wrapper--rounded-corners > zipcode-entry > div > form > div.gateway-login_single-field-wrapper > div.trailer--double > label > div > div.select-field > select')
        cities_entry_first_click.click()
        for cities_entry_second_click in cities_entry_first_click.find_elements_by_tag_name('option'):
            if current_city in cities_entry_second_click.text:
                cities_entry_second_click.click()
                break
        cities_entry_third_click = browser_driver.find_element_by_css_selector('#main-content > div > section.gateway-page_body-content-wrapper.gateway-page_body-content-wrapper--no-margin > div.gateway-body-content_login-wrapper.gateway-body-content_login-wrapper--rounded-corners > zipcode-entry > div > form > div.gateway-login_single-field-wrapper > div.button-container > div.button-container_control.button-container_control--no-outer-spacing.omega > button')
        cities_entry_third_click.click() 
    except:
        pass
    time.sleep(3)
        #GRAB SELENIUM SESSION COOKIES
    selenium_cookies = browser_driver.get_cookies()
        #QUIT SELENIUM BROWSER / RETURN SELENIUM COOKIES
    browser_driver.quit()
    return selenium_cookies
#===================================================================================================================================================
    #SEND GET REQUESTS FOR AVAILABILITY DATA // RETURN RAW JSON DATA DICTIONARY // FUNCTION
def send_get_requests(headers, session):
        #DEFINE RAW DATA DICTIONARY
    raw_data_dictionary = []
        #14 DAY FOR LOOP
    for x in range(13):
        x = x+1
        today = date.today()
        today += datetime.timedelta(days=x)
            #DEFINE GET REQUEST PARAMETERS
        availability_url = 'https://www.peapod.com/api/v2.0/user/slots'
        params = {
            'delivAvail': 'true',
            'headers': 'true',
            'pupAvail': 'true',
            'selected': 'true',
            'serviceType': 'D',
            'viewDate': today
        }
            #SEND GET REQUEST / STORE FULL RESPONSE
        availability_response = session.get(availability_url, headers = headers, params= params)
            #PULL RAW JSON DATA FROM RESPONSE
        availability_json = availability_response.json()
            #APPEND RAW JSON DATA TO DICTIONARY
        raw_data_dictionary.append(availability_json)
        #RETURN RAW DATA DICTIONARY
    return raw_data_dictionary
#===================================================================================================================================================
    #RUN REQUESTS SESSION // RETURN RAW JSON DATA DICTIONARY // FUNCTION
def run_requests_session(selenium_cookies, url, headers):
    with requests.Session() as session:
            #SETUP REQUESTS // PASS SELENIUM COOKIES TO REQUESTS
        for cookie in selenium_cookies:
            session.cookies.set(cookie['name'], cookie['value'])
            #INITIAL REQUESTS LOAD
        response = session.get(url, headers = headers)
            #EXECUTE RAW DATA GET REQUESTS / SAVE RAW DATA DICTIONARY
        raw_data_dictionary = send_get_requests(headers, session)
            #END REQUESTS SESSION
        session.close()    
            #RETURN RAW DATA DICTIONARY
        return raw_data_dictionary
#===================================================================================================================================================
    #AUTO BROWSER FOR SESSION COOKIES // RETURNS SELENIUM SESSION COOKIES // FUNCTION
def get_selenium_cookies(current_zip_code, current_city):
        #DEFINE NEEDED URL/HEADERS
    url = 'https://www.peapod.com'
        #EXECUTE BROWSER SETUP
    browser_driver = selenium_setup()    
        #EXECUTE SELENIUM BROWSER
    selenium_cookies = run_selenium_browser(current_zip_code, current_city, browser_driver, url)
        #RETURN SELENIUM COOKIES
    return selenium_cookies
#===================================================================================================================================================
    #GET REQUESTS FOR RAW AVAILABILITY DATA // RETURNS JSON AVAILABILITY DATA // FUNCTION
def get_raw_availability_data(selenium_cookies):
        #DEFINE NEEDED URL/HEADERS
    url = 'https://www.peapod.com'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'}
        #EXECUTE REQUESTS SESSION
    raw_data_dictionary = run_requests_session(selenium_cookies, url, headers)
        #RETURN RAW DATA DICTIONARY
    return raw_data_dictionary
#===================================================================================================================================================
    #PARSE RAW DATA DICTIONARY // RETURN AVAILABLE DATETIME JSON DATA DICTIONARY // FUNCTION
def parse_raw_json_data(raw_data_dictionary):
        #DEFINE PARSED DATA DICTIONARY
    parsed_data_dictionary = []
        #TRY TO PARSE EACH DATETIME SLOT IN RAW DATA
    try:
            #FOR LOOP FOR EACH OVERALL RAW JSON DATE DATA
        for raw_json_data_date in range(len(raw_data_dictionary)):
                #FOR LOOP FOR EACH TIME SLOT IN A SINGLE RAW JSON DATA DATE
            for slot_number in raw_data_dictionary[raw_json_data_date]['response']['slots']:
                    #IF A SLOT IS NOT SOLD OUT SAVE TIME START, TIME END, AND DATE
                if (slot_number['statusMsg'] != 'Sold Out'):
                    availability_date = slot_number['date']
                    availability_time_start = slot_number['timeStart'] [11:]
                    availability_time_end = slot_number['timeEnd'] [11:]
                    parsing_slot_availability_dictionary = [availability_date, availability_time_start, availability_time_end]
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
        #CHECK AVAILABILITY WITH IF
    if not parsed_availability_dictionary:
        return availability_status
    else:
        availability_status = True
        return availability_status
#===================================================================================================================================================
    #GET THEN PARSE AVAILABILITY DATA // RETURN PARSED AVAILABILITY DICTIONARY // FUNCTION
def get_then_parse_availability_data(selenium_cookies):
        #GET/PARSE RAW AVAILABILITY DATA
    raw_data_dictionary = get_raw_availability_data(selenium_cookies)
        #PARSE RAW AVAILABILITY DATA
    parsed_availability_dictionary = parse_raw_json_data(raw_data_dictionary)
        #RETURN PARSED AVAILABILITY DATA
    return parsed_availability_dictionary
#===================================================================================================================================================
    #PUSH AVAILABLE DATETIMES TO DATABASE // RETURN !!TBD!! // FUNCTION
    
#===================================================================================================================================================
    #MAIN SCRIPT //// GET RAW DATA -> PARSE RAW DATA -> CHECK IF AVAILABLE DATETIMES EXIST IN PARSED DATA -> PUSH AVAILABLE DATETIMES TO DATABASE //// USES ACCOUNT DATABASE INFO FOR ZIP CODES & CITIES //// FUNCTION
def main_Script_Function(Account_Database):
    for x in range(len(Account_Database)):
        current_email = Account_Database[x][0]
        current_zip_code = Account_Database[x][1]
        current_city = Account_Database[x][2]
            #GET AUTO BROWSER SELENIUM SESSION COOKIES
        selenium_cookies = get_selenium_cookies(current_zip_code, current_city)

            #GET THEN PARSE AVAILABILITY DATA
        parsed_availability_dictionary = get_then_parse_availability_data(selenium_cookies)
            #CHECK AVAILABILITY STATUS
        availability_status = availability_status_checker(parsed_availability_dictionary)
            #PRINT AVAILABILITY OR PRINT NOT AVAILABLE
        if availability_status == True:
            print(parsed_availability_dictionary)
        else:
            print('No times or dates available')
#===================================================================================================================================================
#FUNCTION CREATION END



#---------------------------------------------------------------------------------------------------------------------------------------------------



#FUNCTION EXECUTION START
#===================================================================================================================================================
main_Script_Function(create_Account_Database_Array_Function(number_Of_Accounts_Function()))






#===================================================================================================================================================
#FUNCTION EXECUTION END



#---------------------------------------------------------------------------------------------------------------------------------------------------
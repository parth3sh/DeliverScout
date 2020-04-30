#START IMPORTING LIBRARIES
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
from requests.auth import HTTPBasicAuth
    #LXML
from lxml import etree
    #JSON
import json
    #TIME
import time
import datetime
from datetime import date 
from datetime import timedelta 
#END IMPORTING LIBRARIES 

#FUNCTION CREATION START
    #START GETTING USER INPUT 
        #HOW MANY ACCOUNTS
def number_Of_Accounts_Function():
    number_Of_Accounts = int(input('Input the number of accounts you have:'))
    return number_Of_Accounts

        #CREATE USER INFO DATABASE // ENTER ACCOUNT INFO
def create_Account_Database_Array_Function(number_Of_Accounts):
    width, height = 3, number_Of_Accounts
    account_Database_Array = [[0 for x in range(width)] for y in range(height)] 
    print(account_Database_Array)

    for x in range(number_Of_Accounts):
        user_email = input('Input your email for account #' + str(x+1) +':')
        user_zip_code = input('Input your zip code for account #' + str(x+1) + ':')
        user_city = input('Input your city for account #' + str(x+1) + ':')

        account_Database_Array[x][0] = user_email
        account_Database_Array[x][1] = user_zip_code
        account_Database_Array[x][2] = user_city

    print(account_Database_Array)
    return account_Database_Array
    #END GETTING USER INPUT


    #START MAIN SCRIPT
def main_Script_Function(Account_Database):
    for x in range(len(Account_Database)):
        current_email = Account_Database[x][0]
        current_zip_code = Account_Database[x][1]
        current_city = Account_Database[x][2]

        peapod_Notification(current_email, is_Peapod_Available(current_zip_code, current_city))

        print(current_email)
        print(current_zip_code)
        print(current_city)
        print(x)
    #END MAIN SCRIPT


    #START IS PEAPOD AVAILABLE FUNCTION
def is_Peapod_Slot_Available_Function(current_zip_code, current_city):
        #AVAILABILITY VARIABLES
    available_Peapod_Times_Dates = []
    peapod_Availability_Status = False

        #SELENIUM SETUP
    url = 'https://www.peapod.com'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--incognito")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation']) 
    chrome_options.add_experimental_option('useAutomationExtension', False)
        #SELENIUM SETUP // EDIT DRIVER PATH HERE
    browser_driver = webdriver.Chrome(options=chrome_options, executable_path=r'C:\Users\Mason\Desktop\DeliverMeScraper\chromedriver.exe')

        #SELENIUM START // LOAD PEAPOD
    browser_driver.get(url)
    #time.sleep(5)

        #SELENIUM CONTINUE // FIND ELEMENTS
    zip_entry = browser_driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div/main/div/div/section[3]/div[2]/zipcode-entry/div/form/div[2]/div/label/div[1]/input')
    submit_button = browser_driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div/main/div/div/section[3]/div[2]/zipcode-entry/div/form/div[2]/div/label/div[2]/button')

        #SELENIUM CONTINUE // SEND INPUT
    zip_entry.send_keys(current_zip_code)
    submit_button.click()
    time.sleep(2)
        #SELENIUM CONTINUE // IF CITIES INPUT
    try:
            #DEFINE BUTTONS // CLICK BUTTONS
        cities_entry_first_click = browser_driver.find_element_by_css_selector('#main-content > div > section.gateway-page_body-content-wrapper.gateway-page_body-content-wrapper--no-margin > div.gateway-body-content_login-wrapper.gateway-body-content_login-wrapper--rounded-corners > zipcode-entry > div > form > div.gateway-login_single-field-wrapper > div.trailer--double > label > div > div.select-field > select')
        cities_entry_first_click.click()
        for cities_entry_second_click in cities_entry_first_click.find_elements_by_tag_name('option'):
            if cities_entry_second_click.text == current_city:
                cities_entry_second_click.click()
                break
        cities_entry_third_click = browser_driver.find_element_by_css_selector('#main-content > div > section.gateway-page_body-content-wrapper.gateway-page_body-content-wrapper--no-margin > div.gateway-body-content_login-wrapper.gateway-body-content_login-wrapper--rounded-corners > zipcode-entry > div > form > div.gateway-login_single-field-wrapper > div.button-container > div.button-container_control.button-container_control--no-outer-spacing.omega > button')
        cities_entry_third_click.click() 
    except:
        pass

        #SELENIUM GRAB COOKIES // PASS COOKIES TO REQUESTS // START REQUESTS
    time.sleep(3)
    selenium_cookies = browser_driver.get_cookies()

        #START REQUESTS SESSION
    with requests.Session() as session:
                #SETUP REQUESTS // PASS SELENIUM COOKIES TO REQUESTS
            for cookie in selenium_cookies:
                session.cookies.set(cookie['name'], cookie['value'])
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'}

                #INITIAL REQUESTS LOAD
            response = session.get(url, headers = headers)

                #GET REQUESTS FOR AVAIALABILITY
            for x in range(13):
                x = x+1
                today = date.today()
                today += datetime.timedelta(days=x)
                availability_url = 'https://www.peapod.com/api/v2.0/user/slots'
                params = {
                    'delivAvail': 'true',
                    'headers': 'true',
                    'pupAvail': 'true',
                    'selected': 'true',
                    'serviceType': 'D',
                    'viewDate': today
                }
                availability_response = session.get(availability_url, headers = headers, params= params)
                    #GRAB JSON RESPONSE
                availability_json = availability_response.json()
                    #APPEND NEEDED AVAILABILITY INFO TO ARRAY // UPDATE AVAILABILITY STATUS
                try:
                    for slot_number in availability_json['response']['slots']:
                        if (slot_number['statusMsg'] != 'Sold Out'):
                            availability_date = slot_number['date']
                            availability_time_start = slot_number['timeStart'] [11:]
                            availability_time_end = slot_number['timeEnd'] [11:]
                            parsing_slot_availability_dictionary = [availability_date, availability_time_start, availability_time_end]
                            available_Peapod_Times_Dates.append(parsing_slot_availability_dictionary)
                            peapod_Availability_Status = True
                except:
                    print(availability_json)
                    print(availability_response.status_code)
        #END REQUESTS SESSION
    session.close()    
        #SLEEP SELENIUM
    #time.sleep(60)
        #QUIT SELENIUM
    browser_driver.quit()
        #SELENIUM END
        #RETURN STATEMENT CHECK
    if peapod_Availability_Status == True:
        return available_Peapod_Times_Dates
    else:
        return 'No times or dates available'
    #END IS PEAPOD AVAILABLE FUNCTION


    #START PEAPOD NOTIFICATION FUNCTION
    #END PEAPOD NOTIFICATION FUNCTION
#FUNCTION CREATION END


#FUNCTION EXECUTION START
    #main_Script_Function(create_Account_Database_Array_Function(number_Of_Accounts_Function()))
print(is_Peapod_Slot_Available_Function('08510', 'Millstone Township, NJ'))
#FUNCTION EXECUTION END

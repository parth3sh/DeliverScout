#START SCRIPT




#---------------------------------------------------------------------------------------------------------------------------------------------------



#START IMPORTING LIBRARIES
#===================================================================================================================================================
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
    #RUN REPEATED MULTIPROCESSING FOR SLOT DATA //// GET NEXT TWO WEEKS OF DATES DICTIOANRY -> SEND GET REQUESTS FOR RAW DATA -> PARSE RAW DATA FOR OPEN SLOTS -> PRINT AVAILABILITY -> RUN AGAIN EVERY MINUTE //// FUNCTION
def get_parse_print_raw_data (all_selenium_guest_session_cookies):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
    dates_dictionary = create_dates_inquiry_dictionary()
    all_parsed_data_dictionary = []

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
                all_parsed_data_dictionary.append(parsed_availability_dictionary)
            else:
                print('No times or dates available')
            end_time = time.time()
            print("Get requests and parse data runtime: " + str(end_time - start_time))
            print("")
        print("----------------------------------------------------------------------------------------------------------------")
        return all_parsed_data_dictionary
    except:
        print("Error: Cookie expired")
        pass
#===================================================================================================================================================
    #MAIN EXECUTION // EXECUTE MAIN FUNCTION // FUNCTION
def MainScout4(all_selenium_guest_sessions):
    parsed_availability_dictionary = get_parse_print_raw_data(all_selenium_guest_sessions)
    return parsed_availability_dictionary
#===================================================================================================================================================
#FUNCTION CREATION END



#---------------------------------------------------------------------------------------------------------------------------------------------------



#FUNCTION EXECUTION START
#===================================================================================================================================================
#if __name__ == '__main__':
    #MainScout4(all_selenium_guest_sessions)
#===================================================================================================================================================
#FUNCTION EXECUTION END



#---------------------------------------------------------------------------------------------------------------------------------------------------




#END SCRIPT

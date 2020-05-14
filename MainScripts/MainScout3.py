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
    #MAINSCRIPTS
from MainScout2 import MainScout2
from MainScout4 import *
#===================================================================================================================================================
#END IMPORTING LIBRARIES 



#---------------------------------------------------------------------------------------------------------------------------------------------------



#FUNCTION CREATION START
#===================================================================================================================================================
    #MAIN SELENIUN EXECUTION // EXECUTE FUNCTION 2 // FUNCTION
def MainScout3_Selenium():
    all_selenium_guest_sessions = MainScout2()
    return all_selenium_guest_sessions
    #MAIN REQUESTS EXECUTION // EXECUTE FUNCTION 4 // FUNCTION
def MainScout3_Requests(all_selenium_guest_sessions):
    MainScout4(all_selenium_guest_sessions)
    #MAIN EXECUTION // CONTINUOUSLY EXECUTE FUNCTION 3 // FUNCTION
def MainScout3():
    x = 0
    while x < 10:
        try:
            all_selenium_guest_sessions = MainScout3_Selenium()
            x = x+1
        except:
            x = 10
            break
        y = 0
        while y < 60:
            try:
                MainScout3_Requests(all_selenium_guest_sessions)
                y = y+1
                time.sleep(60)
            except:
                y = 60
                break
#===================================================================================================================================================
#FUNCTION CREATION END



#---------------------------------------------------------------------------------------------------------------------------------------------------



#FUNCTION EXECUTION START
#===================================================================================================================================================
if __name__ == '__main__':
    MainScout3()
#===================================================================================================================================================
#FUNCTION EXECUTION END



#---------------------------------------------------------------------------------------------------------------------------------------------------




#END SCRIPT

    

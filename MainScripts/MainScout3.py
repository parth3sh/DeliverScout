#START SCRIPT




#---------------------------------------------------------------------------------------------------------------------------------------------------



#START IMPORTING LIBRARIES
#===================================================================================================================================================
    #TIME
import time
    #MAINSCRIPTS
from MainScout2 import MainScout2
from MainScout4 import MainScout4
from MainScout5 import MainScout5
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
    parased_availability_dictionary = MainScout4(all_selenium_guest_sessions)
    return parased_availability_dictionary
    #MAIN EXECUTION // CONTINUOUSLY EXECUTE FUNCTION 3 // FUNCTION
def MainScout3_Notifications(parsed_availability_dictionary):
    MainScout5(parsed_availability_dictionary)
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
        while y < 180:
            try:
                parsed_availability_dictionary = MainScout3_Requests(all_selenium_guest_sessions)
                y = y+1
            except:
                y = 180
                break
            finally:
                MainScout3_Notifications(parsed_availability_dictionary)
                time.sleep(58.5)
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

    

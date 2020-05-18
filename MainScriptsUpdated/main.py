from MainScout2 import MainScout2
from MainScout4 import MainScout4
import time


import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("C:/Users/Mason/Desktop/DeliverMeScraper/MainScriptsUpdated/deliverscout-firebase-adminsdk-fz84e-455a4eb0be.json")
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://deliverscout.firebaseio.com'
})

#Get database zips and cities
def getData():
    ref = db.reference('zips')
    values = ref.get()
    dataArray = create_Account_Database_Array_Function(len(values), values)
    print(dataArray)
    return dataArray

#Make database data into an array
def create_Account_Database_Array_Function(number_Of_Accounts,values):
    width, height = 2, number_Of_Accounts
    account_Database_Array = [[0 for x in range(width)] for y in range(height)] 
    n = 0
    for key in values:
        user_zip_code = values.get(key)['zip']
        user_city = values.get(key)['city']

        account_Database_Array[n][0] = user_zip_code
        account_Database_Array[n][1] = user_city
        n = n+1
    return account_Database_Array

# Push Slots to Database
def pushSlots(slots):
    ref = db.reference("slots")
    print(slots[0][0])


    for a in range(len(slots)): 
        for b in range((len(slots[a]))):
            ref.push(
                {
                    'day': slots[a][b][0],
                    'start': slots[a][b][1],
                    'end': slots[a][b][2]
                }
        )


def MainScout3_Requests(seleniumSessions):
    parsed_availability_dictionary = MainScout4(seleniumSessions)
    return parsed_availability_dictionary
    #MAIN EXECUTION // CONTINUOUSLY EXECUTE FUNCTION 3 // FUNCTION

def MainScout3_Notifications(parsed_availability_dictionary):
    pushSlots(parsed_availability_dictionary)

#Main execution
if __name__ == '__main__':
    dataArray = getData()

    x = 0
    while x < 10:
        try:
            seleniumSessions = MainScout2(dataArray)
            x = x+1
        except:
            x = 10
            break
        y = 0
        while y < 180:
            try:
                parsed_availability_dictionary = MainScout3_Requests(seleniumSessions)
                y = y+1
            except:
                y = 180
                break
                
            finally:
                pushSlots(parsed_availability_dictionary)
                time.sleep(58.5)



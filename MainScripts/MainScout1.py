#START SCRIPT




#---------------------------------------------------------------------------------------------------------------------------------------------------



#START IMPORTING LIBRARIES
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
#FUNCTION CREATION END



#---------------------------------------------------------------------------------------------------------------------------------------------------




#END SCRIPT
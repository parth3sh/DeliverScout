#START SCRIPT




#---------------------------------------------------------------------------------------------------------------------------------------------------



#START IMPORTING LIBRARIES
#===================================================================================================================================================
    #JSON
import json
    #TWILIO
from twilio.rest import Client
import os
import sendgrid
#===================================================================================================================================================
#END IMPORTING LIBRARIES 



#---------------------------------------------------------------------------------------------------------------------------------------------------



#FUNCTION CREATION START
#===================================================================================================================================================
    #MAIN EXECUTION // EXECUTE MAIN FUNCTION // FUNCTION
def Monitor(parsed_availability_dictionary):
        #CONVERT MULTIDIMENSIONAL ARRAY TO SIMPLE STRING
    text_list = []
    for outermost_layer in range(len(parsed_availability_dictionary)):
        for inner_layer in range(len(parsed_availability_dictionary[outermost_layer])):
            for innermost_layer in range(len(parsed_availability_dictionary[outermost_layer][inner_layer])):
                text_list.append(parsed_availability_dictionary[outermost_layer][inner_layer][innermost_layer])
    text_string = ''.join(str(x) for x in text_list)
        #TWILIO SMS LOGIN/SETUP
    account_sid = 'ACafbb4abcc7af4adb131757c8b1837c96'
    auth_token = 'f541eb48c9d7e3d13e99a5216adee716'
    client = Client(account_sid, auth_token)
        #SEND TWILIO TEXT MESSAGE
    message1 = client.messages \
        .create(
            body = text_string,
            messaging_service_sid="MG4e583732dc92ecd11c1e4f0e73481311",
            to="+19082274958"
        )
    print(message1)
    message2 = client.messages \
        .create(
            body = text_list,
            messaging_service_sid="MG4e583732dc92ecd11c1e4f0e73481311",
            to="+19089077299"
        )
    print(message2)
        #TWILIO EMAIL LOGIN/SETUP
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    data1 = {"personalizations": 
                [{"to": [{"email": "masongrigo@gmail.com"}],
                "subject": "Open Times/Dates"}],

            "from": {"email": "notification@deliverscout.com"},

            "content": [{
                "type": "text/plain",
                "value": text_string}]}
    data2 = {"personalizations": 
                [{"to": [{"email": "parthesh152@gmail.com"}],
                "subject": "Open Times/Dates"}],

            "from": {"email": "notification@deliverscout.com"},
            
            "content": [{
                "type": "text/plain",
                "value": text_string}]}
        #SEND TWILIO/SENDGRID EMAIL MESSAGE
    response1 = sg.client.mail.send.post(request_body=data1)
    print(response1.status_code)
    response2= sg.client.mail.send.post(request_body=data2)
    print(response2.status_code)
#===================================================================================================================================================
#FUNCTION CREATION END



#---------------------------------------------------------------------------------------------------------------------------------------------------



#FUNCTION EXECUTION START
#===================================================================================================================================================
#if __name__ == '__main__':
    #Monitor([[['parsed_availability_dictionary']]])
#===================================================================================================================================================
#FUNCTION EXECUTION END



#---------------------------------------------------------------------------------------------------------------------------------------------------




#END SCRIPT
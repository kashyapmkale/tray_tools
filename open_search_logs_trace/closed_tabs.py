'''
This script was used to cheeck if the tabs for following tab_ids(in excel) are closed or not.
'''

import requests
import json
import time
import openpyxl

prod_url =  "https://logging.production.internal.tray.com/_search"
qa_url = "https://logging.qa.internal.tray.com/_search"

# Set the URL and credentials
url = prod_url
username = "user"
password = ""

# Set the request headers
headers = {
    "Content-Type": "application/json"
}


workbook = openpyxl.load_workbook('closeTabLogTest.xlsx')
worksheet = workbook['Sheet1']
olo_list = worksheet['A']

index = 1
for cell in olo_list:
    a_column = "A"+str(index)
    b_column = "B"+str(index)
    index = index + 1
    if(not cell.value):
        print("----END----")
        break
    time.sleep(1)
    if(index % 20 == 0):
        time.sleep(5)
    try:    
        # Set the JSON data
        data = {
        "query": {
            "query_string": {
            "query": "",
            "default_field": "message"
            }
        },
        "size": 10
        }

        # Extract the value and assign it to a variable
        search_value = str(int(cell.value))

        # Modify the data dictionary with the variable
        data["query"]["query_string"]["query"] = "\"closeTab\" AND \"" + search_value + "\" AND \"requestJSON from closeTab\""
        #print(data["query"]["query_string"]["query"])
        # Convert the data to JSON format
        json_data = json.dumps(data)

        # Make the POST request with basic authentication and JSON body
        response = requests.post(url, headers=headers, auth=(username, password), data=json_data)
        response_data = json.loads(response.text)
        data_dict = dict(response_data)
        #print(data_dict)

        correlation_id = data_dict["hits"]["hits"][0]["_source"]["context"]["CorrelationId"]
        # Print the response
        # print("correlation_id : " + correlation_id)


        time.sleep(1)
        data_updated = {
        "query": {
            "query_string": {
            "query": "",
            "default_operator": "AND"
            }
        },
        "size": 10
        }

        data_updated["query"]["query_string"]["query"] = "context.CorrelationId:" + correlation_id + " AND message:response closeTab"
        # Convert the data to JSON format
        # print(data_updated)
        json_data_updated = json.dumps(data_updated)

        # Make the POST request with basic authentication and JSON body
        response = requests.post(url, headers=headers, auth=(username, password), data=json_data_updated)
        response_data = json.loads(response.text)
        data_dict_updated = dict(response_data)
        #print(data_dict_updated)
        close_tab_message = data_dict_updated["hits"]["hits"][0]["_source"]["message"]
        #print(close_tab_message)

        success_message = "Tab successfully closed"
        if success_message in close_tab_message:
            print(str(int(cell.value)) + " : " + "closeTab successful")
        else:
            print(str(int(cell.value)) + " : " + "closeTab successful")

    except Exception as e:
        # Code to handle other exceptions
        print(str(int(cell.value)) + " : " + "closeTab Call Missing or Error in retriving details")
        print(str(e))


    
'''
Output for the program

27620188 : closeTab successful
27620554 : closeTab successful
27619941 : closeTab Call Missing or Error in retriving details
list index out of range
27619385 : closeTab successful
27621148 : closeTab successful
27619647 : closeTab successful
27619725 : closeTab successful
27620772 : closeTab successful
27620688 : closeTab successful
27687097 : closeTab successful
27686816 : closeTab successful
27613383 : closeTab Call Missing or Error in retriving details
list index out of range
27621227 : closeTab successful
27620220 : closeTab successful
27620957 : closeTab successful
27620488 : closeTab Call Missing or Error in retriving details
list index out of range
27620849 : closeTab Call Missing or Error in retriving details
list index out of range
27621093 : closeTab successful
27617460 : closeTab successful
27686551 : closeTab successful
27619965 : closeTab successful
27618769 : closeTab successful
27621113 : closeTab successful
27610375 : closeTab successful
27620836 : closeTab successful
27620762 : closeTab successful
27620259 : closeTab Call Missing or Error in retriving details
list index out of range
27620526 : closeTab Call Missing or Error in retriving details
list index out of range
27566365 : closeTab successful
27621210 : closeTab successful
27620210 : closeTab Call Missing or Error in retriving details
list index out of range
27686764 : closeTab successful
27620749 : closeTab successful
27619170 : closeTab Call Missing or Error in retriving details
list index out of range
27619702 : closeTab successful
27613116 : closeTab successful
27686477 : closeTab successful
27621055 : closeTab Call Missing or Error in retriving details
list index out of range
27603551 : closeTab successful
27656946 : closeTab successful
27620619 : closeTab successful
----END----

'''

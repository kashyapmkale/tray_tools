'''
This script was used to find out tab_ids against their olo order ids for OLO Orders coming from iOS Application from OpenSearch.
The excel file contains olo order ids.
'''


import requests
import json
import time
import openpyxl

prod_url =  "https://logging.production.internal.tray.com/_search"
qa_url = "https://logging.qa.internal.tray.com/_search"

# Set the URL and credentials
url = prod_url
username = ""
password = ""

# Set the request headers
headers = {
    "Content-Type": "application/json"
}


workbook = openpyxl.load_workbook('log96.xlsx')
worksheet = workbook['Sheet1']
olo_list = worksheet['A']


workbook_op = openpyxl.load_workbook('output.xlsx')
worksheet_op = workbook_op['Sheet1']

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
        search_value = str(cell.value)

        # Modify the data dictionary with the variable
        data["query"]["query_string"]["query"] = "\"/tray/v0/orders request payload\" AND \"" + search_value + "\""

        # Convert the data to JSON format
        json_data = json.dumps(data)

        # Make the POST request with basic authentication and JSON body
        response = requests.post(url, headers=headers, auth=(username, password), data=json_data)
        response_data = json.loads(response.text)
        data_dict = dict(response_data)
        # print(response_data)
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

        data_updated["query"]["query_string"]["query"] = "context.CorrelationId:" + correlation_id + " AND message:Open Tab Id"
        # Convert the data to JSON format
        # print(data_updated)
        json_data_updated = json.dumps(data_updated)

        # Make the POST request with basic authentication and JSON body
        response = requests.post(url, headers=headers, auth=(username, password), data=json_data_updated)
        response_data = json.loads(response.text)
        data_dict_updated = dict(response_data)
        tab_id_message = data_dict_updated["hits"]["hits"][0]["_source"]["message"]

        # Split the string by the colon delimiter
        split_string = tab_id_message.split(':')

        # Extract the integer value
        extracted_value = int(split_string[1].strip())
        print(cell.value + " : " + str(extracted_value))
        worksheet_op[a_column] = cell.value
        worksheet_op[b_column] = str(extracted_value)
        workbook_op.save('output.xlsx')
    except Exception as e:
        # Code to handle other exceptions
        print(cell.value + " : " + "NOT FOUND")
        worksheet_op[a_column] = cell.value
        worksheet_op[b_column] = "NOT FOUND"
        workbook_op.save('output.xlsx')
        print(str(e))

workbook_op.save('output.xlsx')

    

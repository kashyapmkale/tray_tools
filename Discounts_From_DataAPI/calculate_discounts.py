import json
import requests

# Define the URL and headers, Chane it to QA/Stage URL as per your requirement.
discounts_url = "https://stage-api.dine.tray.com/v1/discounts"
revenue_center_url = "https://stage-api.dine.tray.com/v1/revenueCenters"
items_url = "https://stage-api.dine.tray.com/v1/items"

headers = {
    "accept": "application/json",
    "Authorization": "Basic QXBpLUtleTpFN2x6QW5RR0NMV3IybkJQZmxmNU1uRWdxM3lxTHVQTw=="
}

#Change the date and the siteId as per your requirement
site_id = "0018"
disount_date = "2023-03-05"

# Define the query parameters
params = {
    "date": disount_date,
    "siteId": site_id
}

discounts_json_content = ""
rc_json_content = ""
items_json_content = ""

# Send the GET request for discounts_url
response = requests.get(discounts_url, headers=headers, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Parse the response JSON into a Python dictionary
    discounts_json_content = json.loads(response.text)
else:
    print("Request failed with status code:", response.status_code)


# Send the GET request for revenue_center_url
#Not changing query parameter for this as it will ignore the parameters which are not required
response = requests.get(revenue_center_url, headers=headers, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Parse the response JSON into a Python dictionary
    rc_json_content = json.loads(response.text)
else:
    print("Request failed with status code:", response.status_code)


# Send the GET request for items_url
response = requests.get(items_url, headers=headers, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Parse the response JSON into a Python dictionary
    items_json_content = json.loads(response.text)
else:
    print("Request failed with status code:", response.status_code)



training_revenue_centers = set()

for record in rc_json_content["revenueCenters"]:
    if record["trainingMode"] == True:
        training_revenue_centers.add(record["id"])

training_items = set()
training_items_obj = []
for item in items_json_content["items"]:
    if item["revenueCenterId"] in training_revenue_centers:
        training_items.add(item[id])
        print("----------------------------------Training Item-------------------------------")
        print(item)
        print("------------------------------------------------------------------------------")
    else:
        training_items_obj.append(item)

total_discount = 0.00
non_training_discounts = []
for discount in discounts_json_content["discounts"]:
    if discount["itemId"] not in training_items:
        non_training_discounts.append(discount)
        total_discount = total_discount + discount["amount"]
    else:
        print("----------------------------------Training Item Discount-------------------------------")
        print(discount)
        print("------------------------------------------------------------------------------")

total_gross_discount = 0.00
for obj in training_items_obj:
    if obj["isComp"] == True and obj["itemVoided"] == False and obj["voided"] == False:
        total_gross_discount = total_gross_discount + obj["grossPrice"]



print("____________________Total discounts___________________________________________")
print(f"{total_discount:.2f}")


print("____________________Total comp___________________________________________")
#data_dict = json.loads(items_json_content)
print(f"{total_gross_discount:.2f}")

print("____________________Total Discount___________________________________________")
#data_dict = json.loads(items_json_content)
total_discount_final = total_discount + total_gross_discount
print(f"{total_discount_final:.2f}")

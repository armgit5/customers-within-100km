# This program is used to invite any customer within 100km of
# Intercom's Dublin office for some food and drinks.
# The GPS coordinates for our Dublin office are 53.339428, -6.257664.
#
# To run the code, please run python invite_customer.py

from invite_customer_helper import get_customer_id_name_list, get_customer_list

# Read customer json string from json_file line by line
# For each line, convert json string to json customer object
# Store each customer json object in customer_array
customer_list = get_customer_list()


# Intercom location
intercom_office_latlng = {"lat": 53.339428, "lng": -6.257664}



# list of customers' ids and names who are within 100km
# each customer's id and names is represented in
# dictionary in this format {"user_id": id, "name": name}
# ** the list is sorted by User ID in ascending order
customer_id_and_name_list = get_customer_id_name_list(customer_list, intercom_office_latlng)



# Print out the names and user ids of customers who are within 100km
# sorted by User ID in ascending order
print("The customers who are within 100km from Intercom are: \n")
for customer in customer_id_and_name_list:
    print("user_id: ", customer["user_id"], ", name: ", customer["name"])
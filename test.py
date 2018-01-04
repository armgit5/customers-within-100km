# This test program tests the following scenarios:
# * distance function against http://www.onlineconversion.com/map_greatcircle_distance.htm
# * get_customer_id_name_list function - return list of customer within 100km
#   and outside of 100km
# * User ID in ascending order
# * Data Keys and Values
#   -- customer_id_and_name_list's customer should contain user_id and name keys
#   -- get_customer_list function - customer json data key and value should not be empty
#                                   customer user_id should be integer
#                                   customer name should be string
#                                   customer latitude should be string or float
#                                   customer latitude should be string or float
#  To run the code, please run python test.py

from invite_customer_helper import get_distance, get_customer_id_name_list, get_customer_list

############# seed or initial variables used for testing ######################
# distance_ref is from http://www.onlineconversion.com/map_greatcircle_distance.htm
# some customer data taken from the input file
distance_ref1 = 151.543023714973
customer1 = {"latitude": "54.1225", "user_id": 27, "name": "Enid Gallagher", "longitude": "-8.143333"}

distance_ref2 = 44.290822355065814
customer2 = {"latitude": "53.1489345", "user_id": 31, "name": "Alan Behan", "longitude": "-6.8422408"}

distance_ref3 = 23.28732066309904
customer3 = {"latitude": "53.1302756", "user_id": 5, "name": "Nora Dempsey", "longitude": "-6.2397222"}

distance_ref4 = 109.37645542985663
customer4 = {"latitude": "53.807778", "user_id": 28, "name": "Charlie Halligan", "longitude": "-7.714444"}

distance_ref5 = 278.20672215365914
customer5 = {"latitude": "51.999447", "user_id": 14, "name": "Helen Cahill", "longitude": "-9.742744"}

distance_ref6 = 98.87459926458477
customer6 = {"latitude": "53.038056", "user_id": 26, "name": "Stephen McArdle", "longitude": "-7.653889"}

# Intercom location
intercom_office_latlng = {"lat": 53.339428, "lng": -6.257664}

##############################################################


############# Helper function ##################
def close_enough(distance_ref, customer):
    """Compare 2 distances between distance_ref and customer distance
    within 0.001km of accuracy.

    Argument:
    distance_ref -- distance in km calculated from
                    http://www.onlineconversion.com/map_greatcircle_distance.htm
    customer -- customer dictionary data used to calculate distance_from_customer

    Returns:
    distance -- distance in km between 2 points on the map
    """

    customer_lat = float(customer["latitude"])
    customer_lng = float(customer["longitude"])

    distance_from_customer = get_distance(customer_lat,
                 customer_lng,
                 intercom_office_latlng["lat"],
                 intercom_office_latlng["lng"])

    if abs(distance_ref - distance_from_customer) < 0.001:
        return True
    return False

##############################################################



################### Test distance function ##################################
# compare distance get from http://www.onlineconversion.com/map_greatcircle_distance.htm
# as distance_ref and customer distance from get_distance fuction using close_enough
# as a helper function. The 2 distances should be within 0.001km of accuracy
assert close_enough(distance_ref1, customer1), "get_distance fuction is not correct"
assert close_enough(distance_ref2, customer2), "get_distance fuction is not correct"
assert close_enough(distance_ref3, customer3), "get_distance fuction is not correct"
assert close_enough(distance_ref4, customer4), "get_distance fuction is not correct"
assert close_enough(distance_ref5, customer5), "get_distance fuction is not correct"
assert close_enough(distance_ref6, customer6), "get_distance fuction is not correct"

##############################################################



############# Test get_customer_id_name_list function #####################
#
# we know that customer2, customer3, customer6 live WITHIN 100km
# customer_id_and_name_list should CONTAIN customer2, customer3
# customer6 ids.
customer_id_and_name_list = get_customer_id_name_list([customer1, customer2, customer3,
                                                       customer4, customer5, customer6],
                                                      intercom_office_latlng)
id_100_list = [customer2["user_id"], customer3["user_id"], customer6["user_id"]]
for customer_within_100 in customer_id_and_name_list:
    if customer_within_100["user_id"] not in id_100_list:
        assert False, "customer_id_and_name_list returned value is not correct"

# we know that customer3 and customer4 live OUTSIDE of 100km radius
# customer_id_and_name_list should NOT CONTAIN customer1, customer4
# customer5 ids.
id_not_100_list = [customer1["user_id"], customer4["user_id"], customer5["user_id"]]
for customer_within_100 in customer_id_and_name_list:
    if customer_within_100["user_id"] in id_not_100_list:
        assert False, "customer_id_and_name_list returned value is not correct"

##############################################################

################### Test User ID in ascending order ####################
# loop through customer_id_and_name_list
# starting from index 1 to the end of the list
# if next user_id is less than previous user_id
# then we know User ID is not sorted or not sorted
# in ascending order
for i in range(1, len(customer_id_and_name_list)):
    if customer_id_and_name_list[i]["user_id"] < customer_id_and_name_list[i-1]["user_id"]:
        assert False, "user_id is not sorted in ascending order"

##############################################################




################Test customer_id_and_name_list has name and id keys ########################
# test to see if customer_id_and_name_list's
# customer object contains user_id and name keys

for customer in customer_id_and_name_list:
    if not customer["user_id"]:
        assert False, "user_id key or value should not be empty or 0"
    if not customer["name"]:
        assert False, "name key or value should not be empty"

##############################################################




################ Test get_customer_list function ########################
#
# test reading input text data and store each customer data
# in customer_list.
# - customer in customer_list should contain latitude, longitude
# user_id and name keys
customer_list = get_customer_list()
for customer in customer_list:
    if not customer["user_id"]:
        assert False, "user_id key or value should not be empty or 0"
    if not customer["name"]:
        assert False, "name key or value should not be empty"
    if not customer["latitude"]:
        assert False, "latitude key key or value should not be empty"
    if not customer["longitude"]:
        assert False, "longitude key or value should not be empty"

# test customer in customer_list
# customer user_id should be integer
# customer name should be string
# customer latitude should be string or float
# customer latitude should be string or float
for customer in customer_list:
    assert isinstance(customer["user_id"], int), "user_id is not integer"

    assert isinstance(customer["name"], str), "name is not string"

    assert isinstance(customer["latitude"], str) or \
            isinstance(customer["latitude"], float), "latitude is not string or float"

    assert isinstance(customer["longitude"], str) or \
           isinstance(customer["longitude"], float), "longitude is not string or float"

##############################################################

print("ALL TESTS PASSED")
# This is program is helper functions program
# - get_distance in km
# - get_customer_id_name_list returns list of cusotmers' ids and names

import math
import json

def get_distance(lat1, lon1, lat2, lon2):
    """Calculate distance from 2 different points

    Argument:
    lat1 -- latitude of point 1
    lon1 -- longitude of point 1
    lat2 -- latitude of point 2
    lon2 -- longitude of point 2

    Returns:
    distance -- distance in km between 2 points on the map
    """

    # test to see if lat1, lon1, lat2, lon2 are float
    assert isinstance(lat1, float), "lat1 is not float"
    assert isinstance(lon1, float), "lon1 is not float"
    assert isinstance(lat2, float), "lat2 is not float"
    assert isinstance(lon2, float), "lon2 is not float"

    # mean earth radius in km
    R = 6371.0

    # latitude in radian
    rad_lat1 = math.pi * lat1 / 180
    rad_lat2 = math.pi * lat2 / 180

    # difference between longitudes
    theta_r = lon1 - lon2

    # longitudes difference in radius
    rad_theta_r = math.pi * theta_r / 180
    constants = math.sin(rad_lat1) * math.sin(rad_lat2) + math.cos(rad_lat1) * math.cos(rad_lat2) * math.cos(rad_theta_r);
    theta_o = math.acos(constants)

    # distance in km
    distance = R * theta_o

    return distance


def get_customer_id_name_list(customer_list, intercom_office_latlng):
    """Find list of customers' ids and names.
    Each customer's id and names is represented in dictionary
    in the format of {"user_id": id, "name": name}
    (user_id in ascending order)

    Argument:
    customer_list -- Array or list of customer object in json
                    read from the input file
    intercom_office_latlng -- Intercom office lat and lng represented
                    in {"lat": lat, "lng": lng} format

    Returns:
    customer_id_and_name_list -- Array or list of customers' ids and names.
                                Ex. [{"user_id": id, "name": name}, {"user_id": id, "name": name}]
    """



    # List of dictionary of customers' ids and names
    # who are withint 100km
    customer_id_and_name_list = [];

    # Loop through the list of customers
    for customer in customer_list:

        # cast customer's latitude and longitude
        # stored in string to floating point
        customer_lat = float(customer["latitude"])
        customer_lng = float(customer["longitude"])

        # distance between customer's home to
        # Intercom office
        customer_distance = get_distance(customer_lat,
                                     customer_lng,
                                     intercom_office_latlng["lat"],
                                     intercom_office_latlng["lng"])

        # check to make sure customer's distance
        # is within 100km from Intercom off
        if customer_distance <= 100.00:
            # contruct customer dict of id and name
            # append customer dict to customer_id_and_name_list
            customer_id_name_dict = {"user_id": customer["user_id"],
                                     "name": customer["name"]}
            customer_id_and_name_list.append(customer_id_name_dict)

            # using insertion sort to sort the customer_id_name_dict inplace
            # as soon as the newly inserted customer_id_name_dict is added to the list
            # and if it's user_id is more than user_ids in the list, it will get shifted to
            # the left of the list using hole to keep track of the current shifting index
            #
            # knowing that customer_id_and_name_list is already sorted, inserting the next
            # new customer_id_name_dict will take up to O(n) time complexity in the worse case to
            # shift to the left side of customer_id_and_name_list
            hole = len(customer_id_and_name_list) - 1
            newly_inserted_customer = customer_id_and_name_list[hole]
            # compare newly customer_id_name_dict user_id with user_ids in the list
            while hole > 0 and customer_id_and_name_list[hole - 1]["user_id"] > newly_inserted_customer["user_id"]:
                customer_id_and_name_list[hole] = customer_id_and_name_list[hole - 1]
                hole -= 1
            customer_id_and_name_list[hole] = newly_inserted_customer

    return customer_id_and_name_list


def get_customer_list():
    """Read customer's data from the input text file
    convert the text data customer data in json format

    Argument: None

    Returns:
    customer_list -- array or list of customer object in json format or dictionary.
                    Ex. [{"latitude": "53.038056", "user_id": 26, "name": "Stephen McArdle", "longitude": "-7.653889"}]
    """
    json_file = "gistfile1.txt"
    customer_list = []
    with open(json_file, "r") as customers:
        for customer_str in customers:
            customer_json = json.loads(customer_str)
            customer_list.append(customer_json)
    return customer_list
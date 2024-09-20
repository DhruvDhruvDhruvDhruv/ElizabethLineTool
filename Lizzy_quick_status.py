import requests
from pprint import pprint
import json
import pandas as pd
import time
import ctypes

####################################################################################################
##                                          FUNCTIONS
####################################################################################################

def get_elizabeth_line_info(stop_point_id, app_id=None, app_key=None):
    """
    Fetch real-time information for the Elizabeth Line at Acton Main Line station.
    
    Parameters:
    - stop_point_id (str): The StopPoint ID for Acton Main Line (likely '940GZZDMACT').
    - app_id (str): Your TfL API app ID (optional).
    - app_key (str): Your TfL API app key (optional).
    
    Returns:
    - dict: The JSON response containing real-time information about the Elizabeth Line at the station.
    """
    base_url = f"https://api.tfl.gov.uk/Line/elizabeth/Arrivals/{stop_point_id}"
    
    # Parameters for authentication if provided
    params = {}
    if app_id and app_key:
        params['app_id'] = app_id
        params['app_key'] = app_key
    
    try:
        response = requests.get(base_url)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()  # Return the JSON data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def save_json_to_file(data, filename):
    """
    Save the given data to a JSON file.
    
    Parameters:
    - data (dict): The JSON data to save.
    - filename (str): The name of the file to save the data to.
    
    Returns:
    - None
    """
    try:
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)  # Save with pretty formatting
        print(f"Data successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving to file: {e}")

import pandas as pd

def display_next_trains(data):
    """
    Sort the output info by expected arrival in ascending order and display the next 5 unique trains to different destinations in a table.
    
    Parameters:
    - data (list): The JSON data containing the arrival information.

    Returns:
    - None
    """
    # Convert JSON data to a DataFrame
    df = pd.DataFrame(data)
    
    # Convert 'expectedArrival' to datetime for sorting
    df['expectedArrival'] = pd.to_datetime(df['expectedArrival'])
    
    
    # Drop duplicates based on 'destinationName' to get the next 5 unique trains
    # df_unique = df_sorted.drop_duplicates(subset='destinationName').head(5)
    df_unique = df.groupby('destinationName').apply(lambda x: x.nsmallest(5, 'expectedArrival')).reset_index(drop=True)

    # Sort by 'expectedArrival' in ascending order
    df_unique = df_unique.sort_values(by='expectedArrival')

    df_unique["expectedArrival"] = df_unique["expectedArrival"] + pd.Timedelta(hours=time.localtime().tm_isdst)
    df_unique['timeToStation'] = df_unique['timeToStation'].apply(lambda x: f"{(x // 60)+(round((x % 60.0)*2/60.0)/2)} mins")

    # Select and display relevant columns
    return df_unique[['destinationName', 'platformName', 'timeToStation', 'expectedArrival']]

def show_message(text):
    ctypes.windll.user32.MessageBoxW(0, text, "Message", 0x40)

#####################################################################################################
##                                        MAIN LOOP
####################################################################################################

if __name__ == "__main__":
    stop_point_id = "910GACTONML"  # StopPoint ID for Acton Main Line
    app_id = None      # Replace with your actual app_id
    app_key = None      # Replace with your actual app_key
    filename = "test_files/elizabeth_line_info.json"  # Name of the file to save the data to
    save = False

    # Get the Elizabeth Line info in JSON format
    elizabeth_line_info = get_elizabeth_line_info(stop_point_id, app_id, app_key)
    
    if elizabeth_line_info and save:
        save_json_to_file(elizabeth_line_info, filename)
    
    next_trains = display_next_trains(elizabeth_line_info)
    donelist = []
    resultstring = ""
    for index, row in next_trains.iterrows():
        if row["destinationName"] not in donelist:
            donelist.append(row["destinationName"])
            resultstring += (f"\nNext train to {row['destinationName']} is in {row['timeToStation']}\n")

    show_message(resultstring)

    # if elizabeth_line_info:
        # pprint(elizabeth_line_info)

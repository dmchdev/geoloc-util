import argparse
import json
import requests

"""
This application will produce geolocation data for either the "zipcode" or "city, state"
inputs, using Open Weather Geolocation API calls. 
Usage examples:
>> python3 geoloc.py -l "60091" "Los Angeles, CA" "Chicago, IL" -apikey "key"
>> python3 geoloc.py -l "60091" -apikey "key"
>> python3 geoloc.py -l "Wilmette, IL" -apikey
"""
# NOTE: normally, API_KEY would not be included in the source code, especially of a public
# repository. The proper way to do is to store it in a secure place, such as a password manager
# or cloud secrets storage and xtract it programmatically. For example, CircleCI can be
# configured with a secret key env variable.


def geolocation_by_city_state(city: str, state: str, api_key: str, country="US") -> dict:
    """
    Obtain geolocation data by city and state. 
    """
    r = requests.get(
        f"http://api.openweathermap.org/geo/1.0/direct?q={city},{state},{country}&appid={api_key}")
    if 400 <= r.status_code:
        return f"API returned error for this location ({city}, {state}). Response code {r.status_code}({r.reason})"
    else:
        if r.json():
            return r.json()[0]
        else:
            return r.json()


def geolocation_by_zipcode(zipcode: str, api_key: str, country="US") -> dict:
    """
    Obtain geolocation data by zipcode
    """
    r = requests.get(
        f"http://api.openweathermap.org/geo/1.0/zip?zip={zipcode},{country}&appid={api_key}")
    if 400 <= r.status_code:
        return f"API returned error for this location. Response code {r.status_code}({r.reason})"
    else:
        return r.json()

def process_locations(locations: list, api_key: str, verbose = False) -> list:
    """
    Processing each location item received from CLI and calling appropriate API request functions.
    Some user input errors have been covered
    """
    report = []
    for location in locations:
        if "," in location:
            location = location.split(",")
            geolocation_data = geolocation_by_city_state(
                location[0].strip(), location[1].strip(), api_key)
        elif location.isdigit():
            if len(location) != 5:
                geolocation_data = f"Zipcode is too short or too long: {location}"
            else:
                geolocation_data = geolocation_by_zipcode(location, api_key)
        else:
            if " " in location:
                arr = location.split()
                state = arr[-1]
                city = " ".join(arr[0:-1])
                geolocation_data = geolocation_by_city_state(city, state, api_key)
            else:
                geolocation_data = geolocation_by_city_state(location, "", api_key)
        if not verbose and geolocation_data and isinstance(geolocation_data, dict):
            geolocation_data = {k: v for k, v in geolocation_data.items() if k != "local_names"}
        report.append(geolocation_data)
    return report


def main():
    """
    Main 
    """
    parser = argparse.ArgumentParser(
        prog='geoloc.py',
        description="Provides geolocation data for both 'city, state_code' and by zipcode")
    parser.add_argument(
        "-l", "--LOCATIONS",
        nargs="+",
        required=True,
        help="""A single location or a space separated list of locations.
        Each "city, state_code"(e.g "Chicago, IL", comma is mandatory) location must be in quotes.
        Each zipcode location may be with or without quotes.
        Example command:
        >> python3 geoloc.py -l 60091 "Chicago, IL" "Los Angeles, CA" "12345" -apikey "apikeystring"      
        """)
    parser.add_argument(
        "-v", "--VERBOSE",
        action="store_true",
        default=False,
        help="Display full geolocation response with local_names included")
    parser.add_argument(
        "-apikey", "--API_KEY",
        required=True,
        help="Token to the Open Weather API")
    args = parser.parse_args()
    if not args.LOCATIONS:
        print("Please provide location(s)")
        return
    report = process_locations(args.LOCATIONS, args.API_KEY, verbose=args.VERBOSE,)
    print(json.dumps(report, indent=4, ensure_ascii=False))
    return report

if __name__ == '__main__':
    main()

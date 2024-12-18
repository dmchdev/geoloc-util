
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import schemas
import geoloc
from jsonschema import validate
import subprocess


def test_zip():
    schema = schemas.zipcode_response_schema 
    report = geoloc.process_locations(["60091"])
    validate(instance=report, schema=schema)
    assert(report[0]["zip"] == "60091")

def test_single_word_city_state():
    schema = schemas.city_state_response_schema
    report = geoloc.process_locations(["Wilmette, IL"])
    validate(instance=report, schema=schema)
    assert(report[0]["name"] == "Wilmette")

def test_multiple_word_city_state():
    schema = schemas.city_state_response_schema
    report = geoloc.process_locations(["Los Angeles, CA"])
    validate(instance=report, schema=schema)
    assert(report[0]["name"] == "Los Angeles")

def test_missing_comma_city_state():
    schema = schemas.city_state_response_schema
    report = geoloc.process_locations(["Wilmette IL"])
    validate(instance=report, schema=schema)
    assert(report[0]["name"] == "Wilmette")

def test_missing_comma_multiple_word_city_state():
    schema = schemas.city_state_response_schema
    report = geoloc.process_locations(["Los Angeles CA"])
    validate(instance=report, schema=schema)
    assert(report[0]["name"] == "Los Angeles")

def test_multiple_locations():
    schema = schemas.multiple_locations_schema 
    report = geoloc.process_locations(["Wilmette, IL", "60091", "Los Angeles, CA"])
    validate(instance=report, schema=schema)
    assert(report[0]["name"] == "Wilmette")
    assert(report[1]["zip"] == "60091")

def test_zip_too_short():
    report = geoloc.process_locations(["6065"])
    assert("Zipcode is too short or too long" in report[0])

def test_zip_with_letters():
    report = geoloc.process_locations(["605b1"])
    assert(report[0] == [])

def test_nonexistent_city():
    report = geoloc.process_locations(["asdfdas, IL"])
    assert(report[0] == [])
    
def test_nonexistent_state():
    report = geoloc.process_locations(["Chicago, TT"])
    assert(report[0] == [])

def test_incorrect_city_state_combination():
    report = geoloc.process_locations(["New York, CA"])
    assert(report[0] == [])
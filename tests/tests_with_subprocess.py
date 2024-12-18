import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import schemas
import geoloc
from jsonschema import validate
import subprocess
import json

def test_zip():
    r = subprocess.check_output(
        ["python3", "../geoloc.py", "-l", "60091"], text=True)
    report = json.loads(r)
    schema = schemas.zipcode_response_schema 
    validate(instance=report, schema=schema)
    assert(report[0]["zip"] == "60091")

def test_single_word_city_state():
    r = subprocess.check_output(
        ["python3", "../geoloc.py", "-l", "Wilmette, IL"], text=True)
    report = json.loads(r)
    schema = schemas.city_state_response_schema
    validate(instance=report, schema=schema)
    assert(report[0]["name"] == "Wilmette")

def test_multiple_word_city_state():
    r = subprocess.check_output(
        ["python3", "../geoloc.py", "-l", "Los Angeles, CA"], text=True)
    report = json.loads(r)
    schema = schemas.city_state_response_schema
    validate(instance=report, schema=schema)
    assert(report[0]["name"] == "Los Angeles")

def test_missing_comma_city_state():
    r = subprocess.check_output(
        ["python3", "../geoloc.py", "-l", "Wilmette IL"], text=True)
    report = json.loads(r)
    schema = schemas.city_state_response_schema
    validate(instance=report, schema=schema)
    assert(report[0]["name"] == "Wilmette")

def test_missing_comma_multiple_word_city_state():
    r = subprocess.check_output(
        ["python3", "../geoloc.py", "-l", "Los Angeles CA"], text=True)
    report = json.loads(r)
    schema = schemas.city_state_response_schema
    validate(instance=report, schema=schema)
    assert(report[0]["name"] == "Los Angeles")

def test_multiple_locations():
    r = subprocess.check_output(
        ["python3", "../geoloc.py", "-l", "Wilmette, IL", "60091", "Los Angeles, CA"], text=True)
    report = json.loads(r)
    schema = schemas.multiple_locations_schema 
    validate(instance=report, schema=schema)
    assert(report[0]["name"] == "Wilmette")
    assert(report[1]["zip"] == "60091")

def test_zip_too_short():
    r = subprocess.check_output(
        ["python3", "../geoloc.py", "-l", "6065"], text=True)
    report = json.loads(r)
    assert("Zipcode is too short or too long" in report[0])

def test_zip_with_letters():
    r = subprocess.check_output(
        ["python3", "../geoloc.py", "-l", "605b1"], text=True)
    report = json.loads(r)
    assert(report[0] == [])

def test_nonexistent_city():
    r = subprocess.check_output(
        ["python3", "../geoloc.py", "-l", "asdfdas, IL"], text=True)
    report = json.loads(r)
    assert(report[0] == [])
    
def test_nonexistent_state():
    r = subprocess.check_output(
        ["python3", "../geoloc.py", "-l", "Chicago, TT"], text=True)
    report = json.loads(r)
    assert(report[0] == [])

def test_incorrect_city_state_combination():
    r = subprocess.check_output(
        ["python3", "../geoloc.py", "-l", "New York, CA"], text=True)
    report = json.loads(r)
    assert(report[0] == [])
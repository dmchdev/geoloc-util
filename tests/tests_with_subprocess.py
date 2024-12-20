import sys
import os
import schemas
from jsonschema import validate
import subprocess
import json
import platform
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


system = platform.system()

if system == "Windows":
    PY_COMMAND = "python"
elif system == "Linux":
    PY_COMMAND = "python3"
elif system == "Darwin":
    PY_COMMAND = "python3"
else:
    PY_COMMAND = "python3"

def test_zip(request):
    api_key = request.config.getoption("--apikey")
    r = subprocess.check_output(
        [PY_COMMAND, "../src/geoloc/geoloc.py", "-l", "60091", "-apikey", api_key], text=True)
    report = json.loads(r)
    schema = schemas.zipcode_response_schema
    validate(instance=report, schema=schema)
    assert report[0]["zip"] == "60091"

def test_single_word_city_state(request):
    api_key = request.config.getoption("--apikey")
    r = subprocess.check_output(
        [PY_COMMAND, "../src/geoloc/geoloc.py", "-l", "Wilmette, IL", "-apikey", api_key], text=True)
    report = json.loads(r)
    schema = schemas.city_state_response_schema
    validate(instance=report, schema=schema)
    assert report[0]["name"] == "Wilmette"

def test_multiple_word_city_state(request):
    api_key = request.config.getoption("--apikey")
    r = subprocess.check_output(
        [PY_COMMAND, "../src/geoloc/geoloc.py", "-l", "Los Angeles, CA", "-apikey", api_key], text=True)
    report = json.loads(r)
    schema = schemas.city_state_response_schema
    validate(instance=report, schema=schema)
    assert report[0]["name"] == "Los Angeles"

def test_missing_comma_city_state(request):
    api_key = request.config.getoption("--apikey")
    r = subprocess.check_output(
        [PY_COMMAND, "../src/geoloc/geoloc.py", "-l", "Wilmette IL", "-apikey", api_key], text=True)
    report = json.loads(r)
    schema = schemas.city_state_response_schema
    validate(instance=report, schema=schema)
    assert report[0]["name"] == "Wilmette"

def test_missing_comma_multiple_word_city_state(request):
    api_key = request.config.getoption("--apikey")
    r = subprocess.check_output(
        [PY_COMMAND, "../src/geoloc/geoloc.py", "-l", "Los Angeles CA", "-apikey", api_key], text=True)
    report = json.loads(r)
    schema = schemas.city_state_response_schema
    validate(instance=report, schema=schema)
    assert report[0]["name"] == "Los Angeles"

def test_multiple_locations(request):
    api_key = request.config.getoption("--apikey")
    r = subprocess.check_output(
        [PY_COMMAND, "../src/geoloc/geoloc.py", "-l", "Wilmette, IL", "60091", "Los Angeles, CA", "-apikey", api_key], text=True)
    report = json.loads(r)
    schema = schemas.multiple_locations_schema 
    validate(instance=report, schema=schema)
    assert report[0]["name"] == "Wilmette"
    assert report[1]["zip"] == "60091"

def test_zip_too_short(request):
    api_key = request.config.getoption("--apikey")
    r = subprocess.check_output(
        [PY_COMMAND, "../src/geoloc/geoloc.py", "-l", "6065", "-apikey", api_key], text=True)
    report = json.loads(r)
    assert "Zipcode is too short or too long" in report[0]

def test_zip_with_letters(request):
    api_key = request.config.getoption("--apikey")
    r = subprocess.check_output(
        [PY_COMMAND, "../src/geoloc/geoloc.py", "-l", "605b1", "-apikey", api_key], text=True)
    report = json.loads(r)
    assert report[0] == []

def test_nonexistent_city(request):
    api_key = request.config.getoption("--apikey")
    r = subprocess.check_output(
        [PY_COMMAND, "../src/geoloc/geoloc.py", "-l", "asdfdas, IL", "-apikey", api_key], text=True)
    report = json.loads(r)
    assert report[0] == []
    
def test_nonexistent_state(request):
    api_key = request.config.getoption("--apikey")
    r = subprocess.check_output(
        [PY_COMMAND, "../src/geoloc/geoloc.py", "-l", "Chicago, TT", "-apikey", api_key], text=True)
    report = json.loads(r)
    assert report[0] == []

def test_incorrect_city_state_combination(request):
    api_key = request.config.getoption("--apikey")
    r = subprocess.check_output(
        [PY_COMMAND, "../src/geoloc/geoloc.py", "-l", "New York, CA", "-apikey", api_key], text=True)
    report = json.loads(r)
    assert report[0] == []
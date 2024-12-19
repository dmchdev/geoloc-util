import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import schemas
from geoloc import geoloc
from jsonschema import validate
import pytest
import asyncio
import pytest_asyncio

# As this is all mocked, we don't have to use 'request' fixture here to get parameters,
# could just use a random string for the api_key (as on LINE 29). I did this implementation 
# solely for purposes of demonstration multiple fixtures usage in Pytest. 
@pytest.mark.asyncio
async def test_zip(mocker, request):
    api_key = request.config.getoption("--apikey")
    mock_data = {
        "zip": "12345",
        "name": "Schenectady",
        "lat": 42.8142,
        "lon": -73.9396,
        "country": "US"
    }
    mock_response = mocker.MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_data
    mocker.patch("requests.get", return_value=mock_response)
    schema = schemas.zipcode_response_schema 
    report = geoloc.process_locations(["12345"], "randomstring")
    validate(instance=report, schema=schema)
    assert(report[0]["zip"] == "12345")

@pytest.mark.asyncio
async def test_single_word_city_state(mocker, request):
    api_key = request.config.getoption("--apikey")
    mock_data = [{
        "name": "Chicago",
        "lat": 41.8755616,
        "lon": -87.6244212,
        "country": "US",
        "state": "Illinois"
    }]
    mock_response = mocker.MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_data
    mocker.patch("requests.get", return_value=mock_response)
    schema = schemas.zipcode_response_schema 
    schema = schemas.city_state_response_schema
    report = geoloc.process_locations(["Chicago, IL"], api_key)
    validate(instance=report, schema=schema)
    assert(report[0]["name"] == "Chicago")

@pytest.mark.asyncio
async def test_multiple_word_city_state(mocker, request):
    api_key = request.config.getoption("--apikey")
    mock_data = [{
        "name": "Los Angeles",
        "lat": 34.0536909,
        "lon": -118.242766,
        "country": "US",
        "state": "California"
        }]

    mock_response = mocker.MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_data
    mocker.patch("requests.get", return_value=mock_response)
    schema = schemas.city_state_response_schema
    report = geoloc.process_locations(["Los Angeles, CA"], api_key)
    validate(instance=report, schema=schema)
    assert(report[0]["name"] == "Los Angeles")

@pytest.mark.asyncio
async def test_missing_comma_city_state(mocker, request):
    api_key = request.config.getoption("--apikey")
    mock_data = [{
        "name": "Wilmette",
        "lat": 42.0757315,
        "lon": -87.7193768,
        "country": "US",
        "state": "Illinois"
        }]
    mock_response = mocker.MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_data
    mocker.patch("requests.get", return_value=mock_response)
    schema = schemas.city_state_response_schema
    report = geoloc.process_locations(["Wilmette IL"], api_key)
    validate(instance=report, schema=schema)
    assert(report[0]["name"] == "Wilmette")

@pytest.mark.asyncio
async def test_missing_comma_multiple_word_city_state(mocker, request):
    api_key = request.config.getoption("--apikey")
    mock_data = [{
        "name": "Los Angeles",
        "lat": 34.0536909,
        "lon": -118.242766,
        "country": "US",
        "state": "California"
        }]

    mock_response = mocker.MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_data
    mocker.patch("requests.get", return_value=mock_response)
    schema = schemas.city_state_response_schema
    report = geoloc.process_locations(["Los Angeles CA"], api_key)
    validate(instance=report, schema=schema)
    assert(report[0]["name"] == "Los Angeles")

@pytest.mark.asyncio
async def test_multiple_locations(mocker, request):
    api_key = request.config.getoption("--apikey")
    city_state_data = {
        "name": "Los Angeles",
        "lat": 34.0536909,
        "lon": -118.242766,
        "country": "US",
        "state": "California"
        }
    zip_data = {
        "zip": "60091",
        "name": "Wilmette",
        "lat": 42.0765,
        "lon": -87.7246,
        "country": "US"
    }
    mock_response_city_state = mocker.MagicMock()
    mock_response_city_state.return_value = city_state_data
    mocker.patch("geoloc.geoloc.geolocation_by_city_state", return_value=city_state_data)
    mock_response_zip = mocker.MagicMock()
    mock_response_zip.return_value = zip_data
    mocker.patch("geoloc.geoloc.geolocation_by_zipcode", return_value=zip_data)
    schema = schemas.multiple_locations_schema
    report = geoloc.process_locations(["Los Angeles, CA", "60091"], api_key)
    validate(instance=report, schema=schema)
    assert(report[0]["name"] == "Los Angeles")
    assert(report[1]["zip"] == "60091")

@pytest.mark.asyncio
async def test_zip_too_short(request):
    api_key = request.config.getoption("--apikey")
    # no external calls take place, so no mocking here
    report = geoloc.process_locations("6065", api_key)
    assert("Zipcode is too short or too long" in report[0])

@pytest.mark.asyncio
async def test_zip_with_letters(mocker, request):
    api_key = request.config.getoption("--apikey")
    mock_data = []
    mock_response = mocker.MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_data
    mocker.patch("requests.get", return_value=mock_response)
    report = geoloc.process_locations(["605b1"], api_key)
    assert(report[0] == [])

@pytest.mark.asyncio
async def test_nonexistent_city(mocker, request):
    api_key = request.config.getoption("--apikey")
    mock_data = []
    mock_response = mocker.MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_data
    mocker.patch("requests.get", return_value=mock_response)
    report = geoloc.process_locations(["asdfdas, IL"], api_key)
    assert(report[0] == [])

@pytest.mark.asyncio    
async def test_nonexistent_state(mocker, request):
    api_key = request.config.getoption("--apikey")
    mock_data = []
    mock_response = mocker.MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_data
    mocker.patch("requests.get", return_value=mock_response)
    report = geoloc.process_locations(["Chicago, TT"], api_key)
    assert(report[0] == [])

@pytest.mark.asyncio
async def test_incorrect_city_state_combination(mocker, request):
    api_key = request.config.getoption("--apikey")
    mock_data = []
    mock_response = mocker.MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_data
    mocker.patch("requests.get", return_value=mock_response)
    report = geoloc.process_locations(["New York, CA"], api_key)
    assert(report[0] == [])
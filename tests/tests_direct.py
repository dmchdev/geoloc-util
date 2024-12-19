
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import schemas
from geoloc import geoloc
from jsonschema import validate
import subprocess
import pytest
import asyncio
import pytest_asyncio

@pytest.mark.asyncio
async def test_zip(request):
    api_key = request.config.getoption("--apikey")
    schema = schemas.zipcode_response_schema 
    report = geoloc.process_locations(["60091"], api_key)
    validate(instance=report, schema=schema)
    assert(report[0]["zip"] == "60091")

@pytest.mark.asyncio
async def test_single_word_city_state(request):
    api_key = request.config.getoption("--apikey")
    schema = schemas.city_state_response_schema
    report = geoloc.process_locations(["Wilmette, IL"], api_key)
    validate(instance=report, schema=schema)
    assert(report[0]["name"] == "Wilmette")

@pytest.mark.asyncio
async def test_multiple_word_city_state(request):
    api_key = request.config.getoption("--apikey")
    schema = schemas.city_state_response_schema
    report = geoloc.process_locations(["Los Angeles, CA"], api_key)
    validate(instance=report, schema=schema)
    assert(report[0]["name"] == "Los Angeles")

@pytest.mark.asyncio
async def test_missing_comma_city_state(request):
    api_key = request.config.getoption("--apikey")
    schema = schemas.city_state_response_schema
    report = geoloc.process_locations(["Wilmette IL"], api_key)
    validate(instance=report, schema=schema)
    assert(report[0]["name"] == "Wilmette")

@pytest.mark.asyncio
async def test_missing_comma_multiple_word_city_state(request):
    api_key = request.config.getoption("--apikey")
    schema = schemas.city_state_response_schema
    report = geoloc.process_locations(["Los Angeles CA"], api_key)
    validate(instance=report, schema=schema)
    assert(report[0]["name"] == "Los Angeles")

@pytest.mark.asyncio
async def test_multiple_locations(request):
    api_key = request.config.getoption("--apikey")
    schema = schemas.multiple_locations_schema 
    report = geoloc.process_locations(["Wilmette, IL", "60091", "Los Angeles, CA"], api_key)
    validate(instance=report, schema=schema)
    assert(report[0]["name"] == "Wilmette")
    assert(report[1]["zip"] == "60091")

@pytest.mark.asyncio
async def test_zip_too_short(request):
    api_key = request.config.getoption("--apikey")
    report = geoloc.process_locations(["6065"], api_key)
    assert("Zipcode is too short or too long" in report[0])

@pytest.mark.asyncio
async def test_zip_with_letters(request):
    api_key = request.config.getoption("--apikey")
    report = geoloc.process_locations(["605b1"], api_key)
    assert(report[0] == [])

@pytest.mark.asyncio
async def test_nonexistent_city(request):
    api_key = request.config.getoption("--apikey")
    report = geoloc.process_locations(["asdfdas, IL"], api_key)
    assert(report[0] == [])

@pytest.mark.asyncio    
async def test_nonexistent_state(request):
    api_key = request.config.getoption("--apikey")
    report = geoloc.process_locations(["Chicago, TT"], api_key)
    assert(report[0] == [])

@pytest.mark.asyncio
async def test_incorrect_city_state_combination(request):
    api_key = request.config.getoption("--apikey")
    report = geoloc.process_locations(["New York, CA"], api_key)
    assert(report[0] == [])
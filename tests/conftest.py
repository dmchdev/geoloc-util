import os

def pytest_addoption(parser):
    parser.addoption("--apikey", action="store", default=os.environ.get("GEOLOC_API_KEY"), help="API key required to access APIs")

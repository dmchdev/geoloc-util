import os

"""
Configuring pytest
"""
def pytest_addoption(parser):
    """
    Adding option to pytest command line
    """
    parser.addoption(
        "--apikey",
        action="store",
        default=os.environ.get("GEOLOC_API_KEY"),
        help="API key required to access APIs")

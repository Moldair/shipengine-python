from shipengine.addresses import Address
from shipengine import SE_SUCCESS, SE_BAD_REQUEST, SE_CONFLICT, SE_CREATED
from shipengine import SE_INTERNAL, SE_MULTI_STATUS, SE_NO_CONTENT
from shipengine import SE_NOT_ALLOWED, SE_NOT_FOUND, SE_UNAUTHORIZED
from pprint import pprint
import pytest
import vcr
import json

@pytest.fixture
def address():
    x = Address()
    pprint(x.headers)
    return x

@pytest.fixture
def parse_address():
    return {
        "text": "Margie McMiller at 3800 North Lamar suite 200 in austin, tx.  The zip code there is 78652."
    }

@pytest.fixture
def parse_expected_keys():
    data = {
        "score": 0.9122137426845613,
        "address": {
            "name": "Margie McMiller",
            "address_line1": "3800 North Lamar",
            "address_line2": "Suite 200",
            "city_locality": "Austin",
            "state_province": "TX",
            "postal_code": 78652,
            "address_residential_indicator": "unknown"
        },
        "entities": [
            {
            "type": "person",
            "score": 0.9519646137063122,
            "text": "Margie McMiller",
            "start_index": 0,
            "end_index": 14,
            "result": {
                "value": "Margie McMiller"
            }
            },
            {
            "type": "address_line",
            "score": 0.9805313966503588,
            "text": "3800 North Lamar",
            "start_index": 19,
            "end_index": 34,
            "result": {
                "line": 1,
                "value": "3800 North Lamar"
            }
            },
            {
            "type": "number",
            "score": 0.9805313966503588,
            "text": 3800,
            "start_index": 19,
            "end_index": 22,
            "result": {
                "type": "cardinal",
                "value": 3800
            }
            },
            {
            "type": "address_line",
            "score": 1,
            "text": "suite 200",
            "start_index": 36,
            "end_index": 44,
            "result": {
                "line": 2,
                "value": "Suite 200"
            }
            },
            {
            "type": "number",
            "score": 0.9805313966503588,
            "text": 200,
            "start_index": 42,
            "end_index": 44,
            "result": {
                "type": "cardinal",
                "value": 200
            }
            },
            {
            "type": "city_locality",
            "score": 0.9805313966503588,
            "text": "austin",
            "start_index": 49,
            "end_index": 54,
            "result": {
                "value": "Austin"
            }
            },
            {
            "type": "state_province",
            "score": 0.6082904353940255,
            "text": "tx",
            "start_index": 57,
            "end_index": 58,
            "result": {
                "name": "Texas",
                "value": "TX"
            }
            },
            {
            "type": "postal_code",
            "score": 0.9519646137063122,
            "text": 78652,
            "start_index": 84,
            "end_index": 88,
            "result": {
                "value": 78652
            }
            }
        ]
    }
    return data.keys()
@vcr.use_cassette('tests/vcr_cassettes/Address/parse-address.yml', filter_query_parameters=['api_key'], filter_headers=['API-Key'])
def test_Parse_Address(address, parse_address, parse_expected_keys):
    r = address.parse(parse_address)

    if r.status_code != SE_SUCCESS:
        pprint(r.json())
    assert r.status_code == SE_SUCCESS
    if not set(parse_expected_keys).issubset(r.json().keys()):
        pprint(set(parse_expected_keys).difference(r.json().keys()))
    assert set(parse_expected_keys).issubset(r.json()), "All keys should be present"

@pytest.fixture
def validate_address():
    data = [
        {
            "name": "Mickey and Minnie Mouse",
            "phone": "714-781-4565",
            "company_name": "The Walt Disney Company",
            "address_line1": "500 South Buena Vista Street",
            "city_locality": "Burbank",
            "state_province": "CA",
            "postal_code": "91521",
            "country_code": "US"
        }
    ]
    return data

@pytest.fixture
def validate_expected_keys():
    data = [
        {
            "status": "verified",
            "original_address": {
            "name": "Mickey and Minnie Mouse",
            "phone": "714-781-4565",
            "company_name": "The Walt Disney Company",
            "address_line1": "500 South Buena Vista Street",
            "address_line2": "null",
            "address_line3": "null",
            "city_locality": "Burbank",
            "state_province": "CA",
            "postal_code": 91521,
            "country_code": "US",
            "address_residential_indicator": "unknown"
            },
            "matched_address": {
            "name": "MICKEY AND MINNIE MOUSE",
            "phone": "714-781-4565",
            "company_name": "THE WALT DISNEY COMPANY",
            "address_line1": "500 S BUENA VISTA ST",
            "address_line2": "null",
            "address_line3": "null",
            "city_locality": "BURBANK",
            "state_province": "CA",
            "postal_code": "91521-0007",
            "country_code": "US",
            "address_residential_indicator": "no"
            },
            "messages": []
        }
    ]
    return data[0].keys()
@vcr.use_cassette('tests/vcr_cassettes/Address/validate-address.yml', filter_query_parameters=['api_key'], filter_headers=['API-Key'])
def test_Validate_Address(address, validate_address, validate_expected_keys):
    r = address.validate(address=validate_address)

    if r.status_code != SE_SUCCESS:
        pprint(r.json())
    assert r.status_code == SE_SUCCESS
    if not set(validate_expected_keys).issubset(r.json()[0].keys()):
        pprint(set(validate_expected_keys).difference(r.json()[0].keys()))
    assert set(validate_expected_keys).issubset(r.json()[0].keys()), "All keys should be present."
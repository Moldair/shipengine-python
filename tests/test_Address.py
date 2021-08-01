from shipengine.addresses import Address
from shipengine import SE_SUCCESS, SE_BAD_REQUEST, SE_CONFLICT, SE_CREATED
from shipengine import SE_INTERNAL, SE_MULTI_STATUS, SE_NO_CONTENT
from shipengine import SE_NOT_ALLOWED, SE_NOT_FOUND, SE_UNAUTHORIZED
from pprint import pprint
import pytest
import vcr
import json

def test_Address_isverified():
    x = Address()
    x._status = 'verified'

    assert x.isverified()

def test_Address_isnotverified():
    x = Address()
    x._status = 'unverified'

    assert not x.isverified()


@vcr.use_cassette('tests/vcr_cassettes/Address/validate-address.yml', 
                    filter_query_parameters=['api_key'], 
                    filter_headers=['API-Key'])
def test_validate_address():
    test_address = [
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

    sut = Address()
    sut.validate(address=test_address)

    assert sut.isverified()

@vcr.use_cassette('tests/vcr_cassettes/Address/parse-address.yml', 
                    filter_query_parameters=['api_key'], 
                    filter_headers=['API-Key'])
def test_Address_parse_address():
    test_address = "Margie McMiller at 3800 North Lamar suite 200 in austin, tx.  The zip code there is 78652."
    
    sut = Address()
    sut.parse(text=test_address)

    assert not sut.isverified()  # The test address is an unverifiable address.

























#     r = address.parse(parse_address)

#     if r.status_code != SE_SUCCESS:
#         pprint(r.json())
#     assert r.status_code == SE_SUCCESS
#     if not set(parse_expected_keys).issubset(r.json().keys()):
#         pprint(set(parse_expected_keys).difference(r.json().keys()))
#     assert set(parse_expected_keys).issubset(r.json()), "All keys should be present"

# def test_Parse_Address_malformed_input(address):
#     expected_exception = "The text parameter should be a string."
#     inputs = [None, {}, [], ()]
#     for input in inputs:
#         with pytest.raises(Exception) as excinfo:
#             r = address.parse(text=input)
#         assert expected_exception in str(excinfo.value)
        

# @pytest.fixture
# def validate_address():
#     data = [
#         {
#             "name": "Mickey and Minnie Mouse",
#             "phone": "714-781-4565",
#             "company_name": "The Walt Disney Company",
#             "address_line1": "500 South Buena Vista Street",
#             "city_locality": "Burbank",
#             "state_province": "CA",
#             "postal_code": "91521",
#             "country_code": "US"
#         }
#     ]
#     return data

# @pytest.fixture
# def validate_expected_keys():
#     data = [
#         {
#             "status": "verified",
#             "original_address": {
#             "name": "Mickey and Minnie Mouse",
#             "phone": "714-781-4565",
#             "company_name": "The Walt Disney Company",
#             "address_line1": "500 South Buena Vista Street",
#             "address_line2": "null",
#             "address_line3": "null",
#             "city_locality": "Burbank",
#             "state_province": "CA",
#             "postal_code": 91521,
#             "country_code": "US",
#             "address_residential_indicator": "unknown"
#             },
#             "matched_address": {
#             "name": "MICKEY AND MINNIE MOUSE",
#             "phone": "714-781-4565",
#             "company_name": "THE WALT DISNEY COMPANY",
#             "address_line1": "500 S BUENA VISTA ST",
#             "address_line2": "null",
#             "address_line3": "null",
#             "city_locality": "BURBANK",
#             "state_province": "CA",
#             "postal_code": "91521-0007",
#             "country_code": "US",
#             "address_residential_indicator": "no"
#             },
#             "messages": []
#         }
#     ]
#     return data[0].keys()

# @vcr.use_cassette('tests/vcr_cassettes/Address/validate-address.yml', filter_query_parameters=['api_key'], filter_headers=['API-Key'])
# def test_Validate_Address(address, validate_address, validate_expected_keys):
#     r = address.validate(address=validate_address)

#     if r.status_code != SE_SUCCESS:
#         pprint(r.json())
#     assert r.status_code == SE_SUCCESS
#     if not set(validate_expected_keys).issubset(r.json()[0].keys()):
#         pprint(set(validate_expected_keys).difference(r.json()[0].keys()))
#     assert set(validate_expected_keys).issubset(r.json()[0].keys()), "All keys should be present."

# def test_Validate_Address_malformed_address(address):
#     expected_exception = "The address parameter should be a list containing a dictionary."
#     with pytest.raises(Exception) as excinfo:
#         r = address.validate(address=None)
#     assert expected_exception in str(excinfo.value)
    
#     with pytest.raises(Exception) as excinfo:
#         r = address.validate(address="")
#     assert expected_exception in str(excinfo.value)
    
#     with pytest.raises(Exception) as excinfo:
#         r = address.validate(address={})
#     assert expected_exception in str(excinfo.value)
    
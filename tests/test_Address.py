from shipengine.addresses import Address
from shipengine import SE_SUCCESS, SE_BAD_REQUEST, SE_CONFLICT, SE_CREATED
from shipengine import SE_INTERNAL, SE_MULTI_STATUS, SE_NO_CONTENT
from shipengine import SE_NOT_ALLOWED, SE_NOT_FOUND, SE_UNAUTHORIZED
from shipengine import APIKeyMissingError,InvalidCurrency,ImproperDownloadParameter,FileNotFound404
import vcr
import pytest

@pytest.fixture
def sut():
    return Address()

def test_Address_isverified(sut):
    sut._status = 'verified'

    assert sut.isverified()

def test_Address_isnotverified(sut):
    sut._status = 'unverified'

    assert not sut.isverified()


@vcr.use_cassette('tests/vcr_cassettes/Address/validate-address.yml', 
                    filter_query_parameters=['api_key'], 
                    filter_headers=['API-Key'],
                    record_mode='new_episodes')
def test_validate_address(sut):
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

    sut.validate(address=test_address)

    assert sut.isverified()

@vcr.use_cassette('tests/vcr_cassettes/Address/parse-address.yml', 
                    filter_query_parameters=['api_key'], 
                    filter_headers=['API-Key'],
                    record_mode='new_episodes')
def test_Address_parse_address(sut):
    test_address = "Margie McMiller at 3800 North Lamar suite 200 in austin, tx.  The zip code there is 78652."
    
    sut.parse(text=test_address)

    assert not sut.isverified()  # The test address is an unverifiable address.

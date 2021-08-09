from shipengine.carriers import Carrier
from shipengine import SE_SUCCESS, SE_BAD_REQUEST, SE_CONFLICT, SE_CREATED
from shipengine import SE_INTERNAL, SE_MULTI_STATUS, SE_NO_CONTENT
from shipengine import SE_NOT_ALLOWED, SE_NOT_FOUND, SE_UNAUTHORIZED
from shipengine import APIKeyMissingError,InvalidCurrency,ImproperDownloadParameter,FileNotFound404
from pprint import pprint
import pytest
import vcr
import json


@pytest.fixture
def sut():
    return Carrier()

@vcr.use_cassette('tests/vcr_cassettes/Carriers/list_carriers.yml', 
                    filter_query_parameters=['api_key'], 
                    filter_headers=['API-Key'])
def test_list_carriers_added_to_account(sut):
    assert sut.list_carriers()


@vcr.use_cassette('tests/vcr_cassettes/Carriers/get_carrier_by_id.yml', 
                    filter_query_parameters=['api_key'], 
                    filter_headers=['API-Key'])
def test_get_carrier_by_id(sut):
    carrierids = [
        ('se-28529731', False),
        ('se-568501', True),
        ('se-568502', True),
        ('se-568503', True),
    ]

    for id, result in carrierids:
        if result:
            assert sut.get_carrier_by_id(id)
        else:
            assert not sut.get_carrier_by_id(id)

@vcr.use_cassette('tests/vcr_cassettes/Carriers/add_funds_to_carrier.yml', 
                    filter_query_parameters=['api_key'], 
                    filter_headers=['API-Key'])
@pytest.mark.xfail
def test_add_funds_to_carrier(sut):
    test_data = [
        ('se-568501', 0, "usd", True),
        ('se-568501', 0, "dkk", False),
    ]

    for data in test_data:
        pprint(data)
        response = sut.add_funds_to_carrier(id=data[0], amount=data[1], currency=data[2])
        if data[3]:
            assert "balance" in response.keys()
        else:
            assert not response
    
@vcr.use_cassette('tests/vcr_cassettes/Carriers/get_carrier_options.yml', 
                    filter_query_parameters=['api_key'], 
                    filter_headers=['API-Key'])
def test_get_carrier_options(sut):
    carriers = [
        ('se-568501', [
                {
                "name": "contains_alcohol",
                "default_value": "false",
                "description": "string"
                }
            ]
        ),
        ('se-568502',[
                {
                "name": "contains_alcohol",
                "default_value": "false",
                "description": "string"
                }
            ]
        ),
        ('se-568503',[
                {
                "name": "contains_alcohol",
                "default_value": "false",
                "description": "string"
                }
            ]
        ),
    ]
    

    for carrier in carriers:
        assert set(carrier[1][0].keys()).issubset(sut.get_carrier_options(id=carrier[0])[0].keys())

@vcr.use_cassette('tests/vcr_cassettes/Carriers/list_carrier_package_types.yml', 
                    filter_query_parameters=['api_key'], 
                    filter_headers=['API-Key'])
def test_list_carrier_package_types(sut):
    carriers = [
        ('se-568501', [
                {
                "package_id": "se-28529731",
                "package_code": "small_flat_rate_box",
                "name": "laptop_box",
                "description": "Packaging for laptops"
                }
            ]
        ),
        ('se-568502',[
                {
                "package_id": "se-28529731",
                "package_code": "small_flat_rate_box",
                "name": "laptop_box",
                "description": "Packaging for laptops"
                }
            ]
        ),
        ('se-568503',[
                {
                "package_id": "se-28529731",
                "package_code": "small_flat_rate_box",
                "name": "laptop_box",
                "description": "Packaging for laptops"
                }
            ]
        ),
    ]
    

    for carrier in carriers:
        assert set(carrier[1][0].keys()).issubset(sut.list_carrier_package_types(id=carrier[0])[0].keys())

@vcr.use_cassette('tests/vcr_cassettes/Carriers/list_carrier_services.yml', 
                    filter_query_parameters=['api_key'], 
                    filter_headers=['API-Key'])
def test_list_carrier_services(sut):
    carriers = [
        ('se-568501', [
                {
                "carrier_id": "se-28529731",
                "carrier_code": "se-28529731",
                "service_code": "usps_media_mail",
                "name": "USPS First Class Mail",
                "domestic": "true",
                "international": "true",
                "is_multi_package_supported": "true"
                }
            ]
        ),
        ('se-568502',[
                {
                "carrier_id": "se-28529731",
                "carrier_code": "se-28529731",
                "service_code": "usps_media_mail",
                "name": "USPS First Class Mail",
                "domestic": "true",
                "international": "true",
                "is_multi_package_supported": "true"
                }
            ]
        ),
        ('se-568503',[
                {
                "carrier_id": "se-28529731",
                "carrier_code": "se-28529731",
                "service_code": "usps_media_mail",
                "name": "USPS First Class Mail",
                "domestic": "true",
                "international": "true",
                "is_multi_package_supported": "true"
                }
            ]
        ),
    ]
    

    for carrier in carriers:
        assert set(carrier[1][0].keys()).issubset(sut.list_carrier_services(id=carrier[0])[0].keys())
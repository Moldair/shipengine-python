from shipengine import ShipEngine
from shipengine import SE_SUCCESS, SE_BAD_REQUEST, SE_CONFLICT, SE_CREATED
from shipengine import SE_INTERNAL, SE_MULTI_STATUS, SE_NO_CONTENT
from shipengine import SE_NOT_ALLOWED, SE_NOT_FOUND, SE_UNAUTHORIZED
from shipengine import APIKeyMissingError,InvalidCurrency,ImproperDownloadParameter,FileNotFound404
from pprint import pprint
import pytest
import vcr

import shipengine

@pytest.fixture
def sut():
    return ShipEngine()

def test_ShipEngine(sut):
    """Tests ShipEngine base class can be created"""
    
    assert isinstance(sut.headers, dict)

@pytest.fixture
def test_address():
    return [
        {
            "address_line1": "525 S Winchester Blvd",
            "city_locality": "San Jose",
            "state_province": "CA",
            "postal_code": "95128",
            "country_code": "US"
        }
    ]

@pytest.fixture
def post_keys():
    return ['status','original_address', 'matched_address','messages']

## Setup Carriers and test get functions
@pytest.fixture
def carrier_keys():
    return ['carriers','request_id','errors']



@vcr.use_cassette('tests/vcr_cassettes/se-get_carriers.yml', filter_query_parameters=['api_key'], filter_headers=['API-Key'])
@pytest.fixture
def default_carrier(sut,carrier_keys):
    r = sut.get(url='https://api.shipengine.com/v1/carriers')
    assert r.status_code == SE_SUCCESS
    assert set(carrier_keys).issubset(r.json().keys()), "All keys should be in the response."
    return r.json()

## Setup default Shipment and Post function
@vcr.use_cassette('tests/vcr_cassettes/se-post_shipment.yml', filter_query_parameters=['api_key'], filter_headers=['API-Key'])
@pytest.fixture
def default_shipment(sut):
    '''Create Default Shipment for testing'''
    r = sut.post(url='https://api.shipengine.com/v1/shipments', 
        json={
            "shipments": [{
                "service_code": "usps_priority_mail",
                "ship_from": {
                    "name": "John Doe",
                    "company_name": "Example Corp.",
                    "address_line1": "4009 Marathon Blvd",
                    "city_locality": "Austin",
                    "state_province": "TX",
                    "postal_code": "78756",
                    "country_code": "US",
                    "phone": "512-555-5555"
                },
                "ship_to": {
                    "name": "Amanda Miller",
                    "address_line1": "525 S Winchester Blvd",
                    "city_locality": "San Jose",
                    "state_province": "CA",
                    "postal_code": "95128",
                    "country_code": "US"
                },
                "packages": [
                    {
                        "weight": {
                            "value": 17,
                            "unit": "pound"
                        },
                        "dimensions": {
                            "length": 36,
                            "width": 12,
                            "height": 24,
                            "unit": "inch"
                        }
                    }
                ]
            }]
        },
    )
    assert r.status_code == SE_SUCCESS
    return r.json()

## Setup default rate and return id
@pytest.fixture
def rate_keys():
    keys = [
        "shipment_id",
        "carrier_id",
        "service_code",
        "external_order_id",
        "items",
        #"tax_identifiers",
        "external_shipment_id",
        "ship_date",
        "created_at",
        "modified_at",
        "shipment_status",
        "ship_to",
        "ship_from",
        "warehouse_id",
        "return_to",
        "confirmation",
        "customs",
        "advanced_options",
        #"origin_type",
        "insurance_provider",
        "tags",
        "order_source_code",
        "packages",
        "total_weight",
        "rate_response",
    ]
    return keys

@vcr.use_cassette('tests/vcr_cassettes/se_post_rates.yml',  filter_query_parameters=['api_key'], filter_headers=['API-Key'])
@pytest.fixture
def default_rate_id(sut, default_shipment, default_carrier,rate_keys):
    
    data = {
        "shipment_id": default_shipment['shipments'][0]['shipment_id'],
        "rate_options": {
                "carrier_ids": [
                    default_carrier['carriers'][0]['carrier_id'],
                    default_carrier['carriers'][1]['carrier_id']
                ],
                "package_types": [],
                "service_codes": [],
                "calculate_tax_amount": "false",
                "preferred_currency": "usd",
                "is_return": "false"
            }
    }
    r = sut.post(url='https://api.shipengine.com/v1/rates', 
        json=data
    )
    assert r.status_code == SE_SUCCESS
    pprint(set(rate_keys).difference(r.json().keys()))
    
    assert set(rate_keys).issubset(r.json().keys()), "All keys should be in the response."
    return r.json()


@pytest.fixture
def batch_keys():
    keys = [
        "label_layout",
        "label_format",
        "batch_id",
        "batch_number",
        "external_batch_id",
        "batch_notes",
        "created_at",
        "processed_at",
        "errors",
        "warnings",
        "completed",
        "forms",
        "count",
        "batch_shipments_url","batch_labels_url",
        "label_download",
    ]
    return keys

@vcr.use_cassette('tests/vcr_cassettes/se-post_create_batch.yml', filter_query_parameters=['api_key'], filter_headers=['API-Key'])
@pytest.fixture
@pytest.mark.xfail
def batch(sut,default_shipment, default_rate_id, batch_keys):
    data = {
        "external_batch_id": "se-28529731",
        "batch_notes": "This is my batch",
        "shipment_ids": [
            default_shipment['shipments'][0]['shipment_id']
        ],
        "rate_ids": [
            default_rate_id['rate_response']['rates'][0]['rate_id']
        ],
        "warehouse_id": default_shipment['shipments'][0]['shipment_id']
    }
    r = sut.post(url='https://api.shipengine.com/v1/batches',
            json=data,
    )
    pprint(data)
    pprint(r.json())
    assert r.status_code == SE_SUCCESS
    assert set(batch_keys).issubset(r.json().keys()), "All keys should be present."


@vcr.use_cassette('tests/vcr_cassettes/se-manual-delete.yml', filter_query_parameters=['api_key'], filter_headers=['API-Key'])
@pytest.mark.xfail
def test_ShipEngine_delete(sut, batch):

    x = sut.post(url='https://api.shipengine.com/v1/batches', 
        json=batch,
    )
    assert x.status_code == SE_SUCCESS

    r = sut.delete(url='https://api.shipengine.com/v1/batches')

    assert r.status_code == SE_NO_CONTENT
    del x
    del r


@pytest.fixture
def put_keys():
    return ['score', 'address', 'entities']

@vcr.use_cassette('tests/vcr_cassettes/se-manual-put.yml', filter_query_parameters=['api_key'], filter_headers=['API-Key'])
@pytest.mark.xfail
def test_ShipEngine_put(sut, put_keys):
    """Tests ability for ShipEngine to put a request"""
    r = sut.put(url='https://api.shipengine.com/v1/addresses/recognize', 
        json={"text": "Margie McMiller at 3800 North Lamar suite 200 in austin, tx.  The zip code there is 78652."}
    )

    assert r.status_code == SE_SUCCESS
    assert set(put_keys).issubset(r.json().keys()), "All keys should be in the response."


@pytest.fixture
def patch_keys():
    return ['currency','amount']

@vcr.use_cassette('tests/vcr_cassettes/se-manual-patch.yml', filter_query_parameters=['api_key'], filter_headers=['API-Key'])
@pytest.mark.xfail
def test_ShipEngine_patch(sut, patch_keys):
    r = sut.patch(url='https://api.shipengine.com/v1/insurance/shipsurance/add_funds', 
        json={
            'currency': 'usd',
            'amount': 0
        },
    )
    assert r.status_code == SE_SUCCESS ### This fails currently because of API Authorizaion failures, not code failures.
    assert set(patch_keys).issubset(r.json()[0].keys()), "All keys should be in the response."
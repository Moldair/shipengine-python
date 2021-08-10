from shipengine.shipments import Shipment
from shipengine import SE_SUCCESS, SE_BAD_REQUEST, SE_CONFLICT, SE_CREATED
from shipengine import SE_INTERNAL, SE_MULTI_STATUS, SE_NO_CONTENT
from shipengine import SE_NOT_ALLOWED, SE_NOT_FOUND, SE_UNAUTHORIZED
from shipengine import APIKeyMissingError,InvalidCurrency,ImproperDownloadParameter,FileNotFound404, InvalidParameters
from contextlib import contextmanager
import vcr
import pytest

@pytest.fixture
def sut():
    return Shipment()


@contextmanager
def does_not_raise():
    yield

@contextmanager
def returns_true():
    yield True

@contextmanager
def returns_false():
    yield False

@vcr.use_cassette('tests/vcr_cassettes/Shipment/list_shipments.yml', 
                    filter_query_parameters=['api_key'], 
                    filter_headers=['API-Key'],
                    record_mode='new_episodes')
@pytest.mark.parametrize(
    "test_value, expectation",
    [
        ({
            'shipment_status': "",      # Enum: "pending" "processing" "label_purchased" "cancelled"
            'batch_id': "",             # string (se_id) [ 1 .. 25 ] characters ^se(-[a-z0-9]+)+$, Example: batch_id=se-28529731
            'tag': "",                  # string non-empty, Example: tag=Letters_to_santa
            'created_at_start': "",     # string <date-time>, Example: created_at_start=2019-03-12T19:24:13.657Z
            'created_at_end': "",       # string <date-time>, Example: created_at_end=2019-03-12T19:24:13.657Z
            'modified_at_start': "",    # string <date-time>, Example: modified_at_start=2019-03-12T19:24:13.657Z
            'modified_at_end': "",      # string <date-time>, Example: modified_at_end=2019-03-12T19:24:13.657Z
            'page': "",                 # integer >= 1, Default:1
            'page_size': "",            # integer >= 1, Default:25
            'sales_order_id': "",       # string
            'sort_dir': "",             # Enum: "asc" "desc", Default: "desc"
            'sort_by': "",              # Enum: "modified_at" "created_at"
        },  pytest.raises(InvalidParameters)),
        ({'shipment_status': "pending"}, does_not_raise()),
        ({'shipment_status': "processing"}, does_not_raise()),
        ({'shipment_status': "label_purchased"}, does_not_raise()),
        ({'shipment_status': "cancelled"}, does_not_raise()),
        ({'batch_id': ""}, pytest.raises(InvalidParameters)),
        ({'batch_id': "se-1"}, does_not_raise()),
        ({'tag': ""}, pytest.raises(InvalidParameters)),
        ({'tag': "a"}, does_not_raise()),
        ({'created_at_start': ""}, pytest.raises(InvalidParameters)),
        ({'created_at_start': "2019-01-01"}, does_not_raise()),
        ({'created_at_end': ""}, pytest.raises(InvalidParameters)),
        ({'created_at_end': "2021-03-05"}, does_not_raise()),
        ({'modified_at_start': ""}, pytest.raises(InvalidParameters)),
        ({'modified_at_start': "2019-01-01"}, does_not_raise()),
        ({'modified_at_end': ""}, pytest.raises(InvalidParameters)),
        ({'modified_at_end': "2021-03-05"}, does_not_raise()),
        ({'page': 0}, pytest.raises(InvalidParameters)),
        ({'page': 1}, does_not_raise()),
        ({'page_size': 0}, pytest.raises(InvalidParameters)),
        ({'page_size': 30}, does_not_raise()),
        ({'sales_order_id': ""}, pytest.raises(InvalidParameters)),
        ({'sales_order_id': "werwer"}, does_not_raise()),
        ({'sort_dir': "desc"}, does_not_raise()),
        ({'sort_dir': "asc"}, does_not_raise()),
        ({'sort_by': "modified_at"}, does_not_raise()),
        ({'sort_by': "created_at"}, does_not_raise()),
        ("", pytest.raises(InvalidParameters)),
        ([], pytest.raises(InvalidParameters))
    ],
)
def test_list_shipments(sut,test_value, expectation):
    with expectation:
        assert sut.list_shipments(params=test_value) is not None

@vcr.use_cassette('tests/vcr_cassettes/Shipment/get_shipment_by_external_id.yml', 
                    filter_query_parameters=['api_key'], 
                    filter_headers=['API-Key'],
                    record_mode='new_episodes')
@pytest.mark.parametrize(
    "test_value, expectation",
    [
        ({'external_shipment_id': "0bcb569d-1727-4ff9-ab49-b2fec0cee5ae"}, does_not_raise()),
        ({'external_shipment_id': ""}, pytest.raises(InvalidParameters)),
        ("", pytest.raises(InvalidParameters)),
        ([], pytest.raises(InvalidParameters))
    ],
)
def test_get_shipment_by_external_id(sut,test_value, expectation):
    with expectation:
        assert sut.get_shipment_by_external_id(params=test_value) is not None

@vcr.use_cassette('tests/vcr_cassettes/Shipment/get_shipment_by_id.yml', 
                    filter_query_parameters=['api_key'], 
                    filter_headers=['API-Key'],
                    record_mode='new_episodes')
@pytest.mark.parametrize(
    "test_value, expectation",
    [
        ({'shipment_id': ""}, pytest.raises(InvalidParameters)),
        ({'shipment_id': "se-28529731"}, does_not_raise()),
        ("", pytest.raises(InvalidParameters)),
        ([], pytest.raises(InvalidParameters))
    ],
)
def test_get_shipment_by_id(sut,test_value, expectation):
    with expectation:
        assert sut.get_shipment_by_id(params=test_value) is not None


@vcr.use_cassette('tests/vcr_cassettes/Shipment/get_shipment_errors.yml', 
                    filter_query_parameters=['api_key'], 
                    filter_headers=['API-Key'],
                    record_mode='new_episodes')
@pytest.mark.parametrize(
    "test_value, expectation",
    [
        ({'shipment_id': "se-28529731"}, does_not_raise()),
        ({'shipment_id': "se-28529731", 'page': 2, 'pagesize': 24}, does_not_raise()),
        ({'shipment_id': "se-28529731", 'page': -2, 'pagesize': 24}, does_not_raise()), # Page is dropped inside of function
        ({'shipment_id': "se-28529731", 'page': 2, 'pagesize': 0}, does_not_raise()), # Pagesize is dropped inside of function
        ({'shipment_id': ""}, pytest.raises(InvalidParameters)),
        ("", pytest.raises(InvalidParameters)),
        ([], pytest.raises(InvalidParameters))
    ],
)
def test_get_shipment_errors(sut,test_value, expectation):
    with expectation:
        assert sut.get_shipment_errors(params=test_value) is not None


@vcr.use_cassette('tests/vcr_cassettes/Shipment/get_shipment_rates.yml', 
                    filter_query_parameters=['api_key'], 
                    filter_headers=['API-Key'],
                    record_mode='new_episodes')
@pytest.mark.parametrize(
    "test_value, expectation",
    [
        ({'shipment_id': "se-28529731"}, returns_true()),
        ({'shipment_id': "se-28529731", 'created_at_start': '2019-01-01'}, does_not_raise()),
        ({'shipment_id': "se-28529731", 'created_at_start': ''}, returns_true()),
        ({'shipment_id': "se-28529731", 'created_at_start': '2'}, returns_false()), # Technically a valid query, but should return error code
        ({'shipment_id': ""}, pytest.raises(InvalidParameters)),
        ("", pytest.raises(InvalidParameters)),
        ([], pytest.raises(InvalidParameters))
    ],
)
def test_get_shipment_rates(sut,test_value, expectation):
    with expectation:
        assert sut.get_shipment_rates(params=test_value) is not None

@vcr.use_cassette('tests/vcr_cassettes/Shipment/parse_shipping_info.yml', 
                    filter_query_parameters=['api_key'], 
                    filter_headers=['API-Key'],
                    record_mode='new_episodes')
@pytest.mark.parametrize(
    "test_value, test_value2, expectation",
    [
        (
            "I have a 4oz package that's 5x10x14in, and I need to ship it to Margie McMiller at 3800 North Lamar suite 200 in austin, tx 78652. Please send it via USPS first class and require an adult signature. It also needs to be insured for $400.\n",
            None, 
            returns_true()
        ),
        (
            "I have a 4oz package that's 5x10x14in, and I need to ship it to Margie McMiller at 3800 North Lamar suite 200 in austin, tx 78652. Please send it via USPS first class and require an adult signature. It also needs to be insured for $400.\n",
            {"shipment": {
                "service_code": "usps_first_class_mail",
                "ship_from": {
                    "company_name": "My Awesome Store",
                    "phone": "555-555-5555",
                    "address_line1": "587 Shotwell St.",
                    "address_line2": "Suite 201",
                    "city_locality": "San Francisco",
                    "state_province": "CA",
                    "postal_code": 94110,
                    "country_code": "US",
                    "address_residential_indicator": "yes"
                    }
                }
            }
            , returns_true()
        ),
        (
            "",
            None, 
            pytest.raises(InvalidParameters)
        ),
    ],
)
def test_parse_shipping_info(sut,test_value,test_value2, expectation):
    with expectation:
        assert sut.parse_shipping_info(text=test_value,shipment=test_value2) is not None

@vcr.use_cassette('tests/vcr_cassettes/Shipment/update_shipment_by_id.yml', 
                    filter_query_parameters=['api_key'], 
                    filter_headers=['API-Key'],
                    record_mode='new_episodes')
@pytest.mark.parametrize(
    "test_value, test_value2, expectation",
    [
        (
            "se-28529731",
            {
                "carrier_id": "se-28529731",
                "service_code": "usps_first_class_mail",
                "external_order_id": "string",
                "items": [],
                "tax_identifiers": [
                    {
                    "taxable_entity_type": "shipper",
                    "identifier_type": "vat",
                    "issuing_authority": "string",
                    "value": "string"
                    }
                ],
                "external_shipment_id": "string",
                "ship_date": "2018-09-23T00:00:00.000Z",
                "ship_to": {
                    "name": "John Doe",
                    "phone": "+1 204-253-9411 ext. 123",
                    "company_name": "The Home Depot",
                    "address_line1": "1999 Bishop Grandin Blvd.",
                    "address_line2": "Unit 408",
                    "address_line3": "Building #7",
                    "city_locality": "Winnipeg",
                    "state_province": "Manitoba",
                    "postal_code": "78756-3717",
                    "country_code": "CA",
                    "address_residential_indicator": "no"
                },
                "ship_from": {
                    "name": "John Doe",
                    "phone": "+1 204-253-9411 ext. 123",
                    "company_name": "The Home Depot",
                    "address_line1": "1999 Bishop Grandin Blvd.",
                    "address_line2": "Unit 408",
                    "address_line3": "Building #7",
                    "city_locality": "Winnipeg",
                    "state_province": "Manitoba",
                    "postal_code": "78756-3717",
                    "country_code": "CA",
                    "address_residential_indicator": "no"
                },
                "warehouse_id": "se-28529731",
                "return_to": {
                    "name": "John Doe",
                    "phone": "+1 204-253-9411 ext. 123",
                    "company_name": "The Home Depot",
                    "address_line1": "1999 Bishop Grandin Blvd.",
                    "address_line2": "Unit 408",
                    "address_line3": "Building #7",
                    "city_locality": "Winnipeg",
                    "state_province": "Manitoba",
                    "postal_code": "78756-3717",
                    "country_code": "CA",
                    "address_residential_indicator": "no"
                },
                "confirmation": "none",
                "customs": {
                    "contents": "merchandise",
                    "non_delivery": "return_to_sender",
                    "customs_items": []
                },
                "advanced_options": {
                    "bill_to_account": "null",
                    "bill_to_country_code": "CA",
                    "bill_to_party": "recipient",
                    "bill_to_postal_code": "null",
                    "contains_alcohol": "false",
                    "delivered_duty_paid": "false",
                    "dry_ice": "false",
                    "dry_ice_weight": {
                    "value": 0,
                    "unit": "pound"
                    },
                    "non_machinable": "false",
                    "saturday_delivery": "false",
                    "use_ups_ground_freight_pricing": "null",
                    "freight_class": 77.5,
                    "custom_field1": "null",
                    "custom_field2": "null",
                    "custom_field3": "null",
                    "origin_type": "pickup",
                    "shipper_release": "null",
                    "collect_on_delivery": {
                    "payment_type": "any",
                    "payment_amount": {
                        "currency": "usd",
                        "amount": 0
                    }
                    }
                },
                "origin_type": "pickup",
                "insurance_provider": "none",
                "order_source_code": "amazon_ca",
                "packages": [
                    {
                    "package_code": "small_flat_rate_box",
                    "weight": {
                        "value": 0,
                        "unit": "pound"
                    },
                    "dimensions": {
                        "unit": "inch",
                        "length": 0,
                        "width": 0,
                        "height": 0
                    },
                    "insured_value": {
                        "0": {
                        "currency": "usd",
                        "amount": 0
                        },
                        "currency": "usd",
                        "amount": 0
                    },
                    "label_messages": {
                        "reference1": "null",
                        "reference2": "null",
                        "reference3": "null"
                    },
                    "external_package_id": "string"
                    }
                ],
                "validate_address": "no_validation"
            }
            ,returns_true()
        ),
        (
            "",
            None, 
            pytest.raises(InvalidParameters)
        ),
        (
            "",
            {
                "carrier_id": "se-28529731",
                "service_code": "usps_first_class_mail",
                "external_order_id": "string",
                "items": [],
                "tax_identifiers": [
                    {
                    "taxable_entity_type": "shipper",
                    "identifier_type": "vat",
                    "issuing_authority": "string",
                    "value": "string"
                    }
                ],
                "external_shipment_id": "string",
                "ship_date": "2018-09-23T00:00:00.000Z",
                "ship_to": {
                    "name": "John Doe",
                    "phone": "+1 204-253-9411 ext. 123",
                    "company_name": "The Home Depot",
                    "address_line1": "1999 Bishop Grandin Blvd.",
                    "address_line2": "Unit 408",
                    "address_line3": "Building #7",
                    "city_locality": "Winnipeg",
                    "state_province": "Manitoba",
                    "postal_code": "78756-3717",
                    "country_code": "CA",
                    "address_residential_indicator": "no"
                },
                "ship_from": {
                    "name": "John Doe",
                    "phone": "+1 204-253-9411 ext. 123",
                    "company_name": "The Home Depot",
                    "address_line1": "1999 Bishop Grandin Blvd.",
                    "address_line2": "Unit 408",
                    "address_line3": "Building #7",
                    "city_locality": "Winnipeg",
                    "state_province": "Manitoba",
                    "postal_code": "78756-3717",
                    "country_code": "CA",
                    "address_residential_indicator": "no"
                },
                "warehouse_id": "se-28529731",
                "return_to": {
                    "name": "John Doe",
                    "phone": "+1 204-253-9411 ext. 123",
                    "company_name": "The Home Depot",
                    "address_line1": "1999 Bishop Grandin Blvd.",
                    "address_line2": "Unit 408",
                    "address_line3": "Building #7",
                    "city_locality": "Winnipeg",
                    "state_province": "Manitoba",
                    "postal_code": "78756-3717",
                    "country_code": "CA",
                    "address_residential_indicator": "no"
                },
                "confirmation": "none",
                "customs": {
                    "contents": "merchandise",
                    "non_delivery": "return_to_sender",
                    "customs_items": []
                },
                "advanced_options": {
                    "bill_to_account": "null",
                    "bill_to_country_code": "CA",
                    "bill_to_party": "recipient",
                    "bill_to_postal_code": "null",
                    "contains_alcohol": "false",
                    "delivered_duty_paid": "false",
                    "dry_ice": "false",
                    "dry_ice_weight": {
                    "value": 0,
                    "unit": "pound"
                    },
                    "non_machinable": "false",
                    "saturday_delivery": "false",
                    "use_ups_ground_freight_pricing": "null",
                    "freight_class": 77.5,
                    "custom_field1": "null",
                    "custom_field2": "null",
                    "custom_field3": "null",
                    "origin_type": "pickup",
                    "shipper_release": "null",
                    "collect_on_delivery": {
                    "payment_type": "any",
                    "payment_amount": {
                        "currency": "usd",
                        "amount": 0
                    }
                    }
                },
                "origin_type": "pickup",
                "insurance_provider": "none",
                "order_source_code": "amazon_ca",
                "packages": [
                    {
                    "package_code": "small_flat_rate_box",
                    "weight": {
                        "value": 0,
                        "unit": "pound"
                    },
                    "dimensions": {
                        "unit": "inch",
                        "length": 0,
                        "width": 0,
                        "height": 0
                    },
                    "insured_value": {
                        "0": {
                        "currency": "usd",
                        "amount": 0
                        },
                        "currency": "usd",
                        "amount": 0
                    },
                    "label_messages": {
                        "reference1": "null",
                        "reference2": "null",
                        "reference3": "null"
                    },
                    "external_package_id": "string"
                    }
                ],
                "validate_address": "no_validation"
            }, 
            pytest.raises(InvalidParameters)
        ),
    ],
)
def test_update_shipment_by_id(sut,test_value,test_value2, expectation):
    with expectation:
        assert sut.update_shipment_by_id(shipment_id=test_value,data=test_value2) is not None

@vcr.use_cassette('tests/vcr_cassettes/Shipment/cancel_shipment_by_id.yml', 
                    filter_query_parameters=['api_key'], 
                    filter_headers=['API-Key'],
                    record_mode='new_episodes')
@pytest.mark.parametrize(
    "test_value, expectation",
    [
        ("se-28529731", returns_true()),
        ("se-285297312222222222223", returns_false()),
        ("se-28529731222222222222332234", pytest.raises(InvalidParameters)),
        ("", pytest.raises(InvalidParameters)),
    ],
)
def test_cancel_shipment_by_id(sut,test_value, expectation):
    with expectation:
        assert sut.cancel_shipment_by_id(shipment_id=test_value) is not None

@vcr.use_cassette('tests/vcr_cassettes/Shipment/add_tag.yml', 
                    filter_query_parameters=['api_key'], 
                    filter_headers=['API-Key'],
                    record_mode='new_episodes')
@pytest.mark.parametrize(
    "test_value, test_value2, expectation",
    [
        ("se-28529731", "Fragile", returns_true()),
        ("se-285297312222222222223", "International", returns_false()),
        ("se-28529731222222222222332234", "Fragile", pytest.raises(InvalidParameters)),
        ("se-28529731", "", pytest.raises(InvalidParameters)),
        ("", "", pytest.raises(InvalidParameters)),
    ],
)
def test_add_tag(sut, test_value, test_value2, expectation):
    with expectation:
        assert sut.add_tag(shipment_id=test_value, tag_name=test_value2) is not None

@vcr.use_cassette('tests/vcr_cassettes/Shipment/remove_tag.yml', 
                    filter_query_parameters=['api_key'], 
                    filter_headers=['API-Key'],
                    record_mode='new_episodes')
@pytest.mark.parametrize(
    "test_value, test_value2, expectation",
    [
        ("se-28529731", "Fragile", returns_true()),
        ("se-285297312222222222223", "International", returns_false()),
        ("se-28529731222222222222332234", "Fragile", pytest.raises(InvalidParameters)),
        ("se-28529731", "", pytest.raises(InvalidParameters)),
        ("", "", pytest.raises(InvalidParameters)),
    ],
)
def test_remove_tag(sut, test_value, test_value2, expectation):
    with expectation:
        assert sut.remove_tag(shipment_id=test_value, tag_name=test_value2) is not None


@vcr.use_cassette('tests/vcr_cassettes/Shipment/create_shipments.yml', 
                    filter_query_parameters=['api_key'], 
                    filter_headers=['API-Key'],
                    record_mode='new_episodes')
@pytest.mark.parametrize(
    "test_value, expectation",
    [
        ("", pytest.raises(InvalidParameters)),
        ({
                    'carrier_id': "se-123890",
                    'service_code': "usps_first_class_mail",
                    'ship_to': {
                        'name': 'John Doe',
                        'phone':'1234567890',
                        'address_line1':'123 Easy Street',
                        'city_locality': 'Beverly Hills',
                        'state_province': 'CA',
                        'postal_code': '90210',
                        'country_code': 'US',
                        'address_residential_indicator': 'yes'                        
                    },
                    'ship_from': {
                        'name': 'ABC Company, LLC',
                        'phone':'7890123456',
                        'address_line1':'42 Answer way',
                        'city_locality': 'Glasgow',
                        'state_province': 'KY',
                        'postal_code': '42141',
                        'country_code': 'US',
                        'address_residential_indicator': 'yes'                        
                    },
                    'packages': [
                        {
                            'package_code': 'package',
                            'weight': {
                                'value': 16.0,
                                'unit': "ounce"
                            },
                        },
                    ],
                },
            returns_true()
        ),
        (
            [
                {
                    'carrier_id': "se-123890",
                    'service_code': "usps_first_class_mail",
                    'ship_to': {
                        'name': 'John Doe',
                        'phone':'1234567890',
                        'address_line1':'123 Easy Street',
                        'city_locality': 'Beverly Hills',
                        'state_province': 'CA',
                        'postal_code': '90210',
                        'country_code': 'US',
                        'address_residential_indicator': 'yes'                        
                    },
                    'ship_from': {
                        'name': 'ABC Company, LLC',
                        'phone':'7890123456',
                        'address_line1':'42 Answer way',
                        'city_locality': 'Glasgow',
                        'state_province': 'KY',
                        'postal_code': '42141',
                        'country_code': 'US',
                        'address_residential_indicator': 'yes'                        
                    },
                    'packages': [
                        {
                            'package_code': 'package',
                            'weight': {
                                'value': 16.0,
                                'unit': "ounce"
                            },
                        },
                    ],
                },
            ], 
            returns_true()
        ),
        (
            [
                {
                    'service_code': "usps_first_class_mail",
                    'ship_to': {
                        'name': 'John Doe',
                        'phone':'1234567890',
                        'address_line1':'123 Easy Street',
                        'city_locality': 'Beverly Hills',
                        'state_province': 'CA',
                        'postal_code': '90210',
                        'country_code': 'US',
                        'address_residential_indicator': 'yes'                        
                    },
                    'ship_from': {
                        'name': 'ABC Company, LLC',
                        'phone':'7890123456',
                        'address_line1':'42 Answer way',
                        'city_locality': 'Glasgow',
                        'state_province': 'KY',
                        'postal_code': '42141',
                        'country_code': 'US',
                        'address_residential_indicator': 'yes'                        
                    },
                    'packages': [
                        {
                            'package_code': 'package',
                            'weight': {
                                'value': 16.0,
                                'unit': "ounce"
                            },
                        },
                    ],
                },
            ], 
            returns_false()
        ),
    ],
)
def test_create_shipments(sut, test_value, expectation):
    
    with expectation:
        assert sut.create_shipment(shipments=test_value) is not None

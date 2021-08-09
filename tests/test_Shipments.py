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








# @vcr.use_cassette('tests/vcr_cassettes/Shipment/create_shipments.yml', 
#                     filter_query_parameters=['api_key'], 
#                     filter_headers=['API-Key'],
#                     record_mode='new_episodes')
# @pytest.mark.parametrize(
#     "test_value, expectation",
#     [
#         ("", pytest.raises(ImproperDownloadParameter)),
#         ("/1/1/3TidbpFJOkm4RmWzQ-woyQ/label-147980607.pdf", pytest.raises(ImproperDownloadParameter)),
#         ("/1/9HYicTGmJEaIECkBSoH1_Q/label-51582669.pdf", pytest.raises(FileNotFound404)),
#         (label_download_endpoint, does_not_raise())
#     ],
# )
# def test_create_shipments(sut, test_value, expectation):
    
#     with expectation:
#         assert sut.create_shipment(filespec=test_value) is not None

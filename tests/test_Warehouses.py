from shipengine.warehouses import Warehouse
from shipengine import SE_SUCCESS, SE_BAD_REQUEST, SE_CONFLICT, SE_CREATED
from shipengine import SE_INTERNAL, SE_MULTI_STATUS, SE_NO_CONTENT
from shipengine import SE_NOT_ALLOWED, SE_NOT_FOUND, SE_UNAUTHORIZED
from shipengine import APIKeyMissingError,InvalidCurrency,ImproperDownloadParameter,FileNotFound404, InvalidParameters
from contextlib import contextmanager
import vcr
import pytest

@pytest.fixture
def sut():
    return Warehouse()


@contextmanager
def does_not_raise():
    yield

@contextmanager
def returns_true():
    yield True

@contextmanager
def returns_false():
    yield False

@vcr.use_cassette('tests/vcr_cassettes/Warehouse/list_warehouses.yml', 
                    filter_query_parameters=['api_key'], 
                    filter_headers=['API-Key'],
                    record_mode='new_episodes')
@pytest.mark.parametrize(
    "test_value, expectation",
    [
        ("",  returns_true()),
    ],
)
def test_list_warehouses(sut,test_value, expectation):
    with expectation:
        assert sut.list_warehouses() is not None


@vcr.use_cassette('tests/vcr_cassettes/Warehouse/create_warehouse.yml', 
                    filter_query_parameters=['api_key'], 
                    filter_headers=['API-Key'],
                    record_mode='new_episodes')
@pytest.mark.parametrize(
    "test_value, expectation",
    [
        (
            {
                'name': "Home",
                'origin_address': {
                        'name': 'ABC Company, LLC',
                        'phone':'7890123456',
                        'address_line1':'42 Answer way',
                        'city_locality': 'Glasgow',
                        'state_province': 'KY',
                        'postal_code': '42141',
                        'country_code': 'US',
                        'address_residential_indicator': 'yes'                        
                    },
                'return_address': {
                        'name': 'ABC Company, LLC',
                        'phone':'7890123456',
                        'address_line1':'42 Answer way',
                        'city_locality': 'Glasgow',
                        'state_province': 'KY',
                        'postal_code': '42141',
                        'country_code': 'US',
                        'address_residential_indicator': 'yes'                        
                    }
            }, returns_true()
        ),
        (
            {
                'name': "Home",
                'origin_address': {
                        'name': 'ABC Company, LLC',
                        'phone':'7890123456',
                        'address_line1':'42 Answer way',
                        'city_locality': 'Glasgow',
                        'state_province': 'KY',
                        'postal_code': '42141',
                        'country_code': 'US',
                        'address_residential_indicator': 'yes'                        
                    }
            }, returns_true()
        ),
        ({'name': "Home"}, returns_false()),
        ({'origin_address': {
                        'name': 'ABC Company, LLC',
                        'phone':'7890123456',
                        'address_line1':'42 Answer way',
                        'city_locality': 'Glasgow',
                        'state_province': 'KY',
                        'postal_code': '42141',
                        'country_code': 'US',
                        'address_residential_indicator': 'yes'                        
                    }}, returns_false()),
        ("", pytest.raises(InvalidParameters)),
        ([], pytest.raises(InvalidParameters))
    ],
)
def test_create_warehouse(sut,test_value, expectation):
    with expectation:
        assert sut.create_warehouse(warehouse_data=test_value) is not None

@vcr.use_cassette('tests/vcr_cassettes/Warehouse/get_warehouse_by_id.yml', 
                    filter_query_parameters=['api_key'], 
                    filter_headers=['API-Key'],
                    record_mode='new_episodes')
@pytest.mark.parametrize(
    "test_value, expectation",
    [
        ("se-2440256", returns_true()),
        ("se-244025234234246", returns_false()),
        ("", pytest.raises(InvalidParameters)),
        ([], pytest.raises(InvalidParameters))
    ],
)
def test_get_warehouse_by_id(sut,test_value, expectation):
    with expectation:
        assert sut.get_warehouse_by_id(warehouse_id=test_value) is not None

@vcr.use_cassette('tests/vcr_cassettes/Warehouse/update_warehouse_by_id.yml', 
                    filter_query_parameters=['api_key'], 
                    filter_headers=['API-Key'],
                    record_mode='new_episodes')
@pytest.mark.parametrize(
    "test_value, test_value2, expectation",
    [
        ("se-2440256",
            {
                'name': "Home",
                'origin_address': {
                        'name': 'ABC Company, LLC',
                        'phone':'7890123456',
                        'address_line1':'42 Answer way',
                        'city_locality': 'Glasgow',
                        'state_province': 'KY',
                        'postal_code': '42141',
                        'country_code': 'US',
                        'address_residential_indicator': 'yes'                        
                    },
                'return_address': {
                        'name': 'ABC Company, LLC',
                        'phone':'7890123456',
                        'address_line1':'42 Answer way',
                        'city_locality': 'Glasgow',
                        'state_province': 'KY',
                        'postal_code': '42141',
                        'country_code': 'US',
                        'address_residential_indicator': 'yes'                        
                    }
            }, returns_true()
        ),
        ("se-2440256",
            {
                'name': "Home",
                'origin_address': {
                        'name': 'ABC Company, LLC',
                        'phone':'7890123456',
                        'address_line1':'42 Answer way',
                        'city_locality': 'Glasgow',
                        'state_province': 'KY',
                        'postal_code': '42141',
                        'country_code': 'US',
                        'address_residential_indicator': 'yes'                        
                    }
            }, returns_true()
        ),
        ("se-2440256", {'name': "Home"}, returns_false()),
        ("se-2440256", {'origin_address': {
                        'name': 'ABC Company, LLC',
                        'phone':'7890123456',
                        'address_line1':'42 Answer way',
                        'city_locality': 'Glasgow',
                        'state_province': 'KY',
                        'postal_code': '42141',
                        'country_code': 'US',
                        'address_residential_indicator': 'yes'                        
                    }}, returns_false()),
        ("", "", pytest.raises(InvalidParameters)),
        ("", [], pytest.raises(InvalidParameters))
    ],
)
def test_update_warehouse_by_id(sut,test_value, test_value2, expectation):
    with expectation:
        assert sut.update_warehouse_by_id(warehouse_id=test_value, warehouse_data=test_value2) is not None


@vcr.use_cassette('tests/vcr_cassettes/Warehouse/delete_warehouse_by_id.yml', 
                    filter_query_parameters=['api_key'], 
                    filter_headers=['API-Key'],
                    record_mode='new_episodes')
@pytest.mark.parametrize(
    "test_value, expectation",
    [
        ("se-2440256", returns_true()),
        ("se-2852973165616843131384684613134", pytest.raises(InvalidParameters)),
        ("se-2852973100000000", returns_false()),
        ("", pytest.raises(InvalidParameters)),
        ([], pytest.raises(InvalidParameters))
    ],
)
def test_delete_warehouse_by_id(sut,test_value, expectation):
    with expectation:
        assert sut.delete_warehouse_by_id(warehouse_id=test_value) is not None

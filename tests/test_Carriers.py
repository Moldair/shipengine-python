from shipengine.carriers import Carrier
from shipengine import SE_SUCCESS, SE_BAD_REQUEST, SE_CONFLICT, SE_CREATED
from shipengine import SE_INTERNAL, SE_MULTI_STATUS, SE_NO_CONTENT
from shipengine import SE_NOT_ALLOWED, SE_NOT_FOUND, SE_UNAUTHORIZED
from shipengine import APIKeyMissingError,InvalidCurrency,ImproperDownloadParameter,FileNotFound404, InvalidParameters
from contextlib import contextmanager
from pprint import pprint
import vcr
import pytest

@pytest.fixture
def sut():
    return Carrier()


@contextmanager
def does_not_raise():
    yield

@contextmanager
def returns_true():
    yield True

@contextmanager
def returns_false():
    yield False


@pytest.fixture
def sut():
    return Carrier()

@vcr.use_cassette('tests/vcr_cassettes/Carriers/list_carriers.yml', 
                    filter_query_parameters=['api_key'], 
                    filter_headers=['API-Key'],
                    record_mode='new_episodes')
def test_list_carriers_added_to_account(sut):
    assert sut.list_carriers()


@vcr.use_cassette('tests/vcr_cassettes/Carriers/get_carrier_by_id.yml', 
                    filter_query_parameters=['api_key'], 
                    filter_headers=['API-Key'],
                    record_mode='new_episodes')
@pytest.mark.parametrize(
    "test_value, expectation",
    [
        ("se-568501", returns_true()),
        ("se-568502", returns_true()),
        ("se-568503", returns_true()),
        ("se-28529731", returns_true()),
        ("", pytest.raises(InvalidParameters)),
    ],
)
def test_get_carrier_by_id(sut, test_value, expectation):
    with expectation:
        assert sut.get_carrier_by_id(carrier_id=test_value) is not None

@vcr.use_cassette('tests/vcr_cassettes/Carriers/add_funds_to_carrier.yml', 
                    filter_query_parameters=['api_key'], 
                    filter_headers=['API-Key'],
                    record_mode='new_episodes')
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
                    filter_headers=['API-Key'],
                    record_mode='new_episodes')
@pytest.mark.parametrize(
    "test_value, expectation",
    [
        ("se-568501", returns_true()),
        ("se-568502", returns_true()),
        ("se-568503", returns_true()),
        ("", pytest.raises(InvalidParameters)),
    ],
)
def test_get_carrier_options(sut, test_value, expectation):
    with expectation:
        assert sut.get_carrier_options(carrier_id=test_value) is not None
    

@vcr.use_cassette('tests/vcr_cassettes/Carriers/list_carrier_package_types.yml', 
                    filter_query_parameters=['api_key'], 
                    filter_headers=['API-Key'],
                    record_mode='new_episodes')
@pytest.mark.parametrize(
    "test_value, expectation",
    [
        ("se-568501", returns_true()),
        ("se-568502", returns_true()),
        ("se-568503", returns_true()),
        ("", pytest.raises(InvalidParameters)),
    ],
)
def test_list_carrier_package_types(sut, test_value, expectation):
    with expectation:
        assert sut.list_carrier_package_types(carrier_id=test_value) is not None

@vcr.use_cassette('tests/vcr_cassettes/Carriers/list_carrier_services.yml', 
                    filter_query_parameters=['api_key'], 
                    filter_headers=['API-Key'],
                    record_mode='new_episodes')
@pytest.mark.parametrize(
    "test_value, expectation",
    [
        ("se-568501", returns_true()),
        ("se-568502", returns_true()),
        ("se-568503", returns_true()),
        ("", pytest.raises(InvalidParameters)),
    ],
)
def test_list_carrier_services(sut, test_value, expectation):
    with expectation:
        assert sut.list_carrier_services(carrier_id=test_value) is not None
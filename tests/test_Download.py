from shipengine.shipengine import ShipEngine
import shipengine
from shipengine.downloads import Download, FileNotFound404, ImproperDownloadParameter
from shipengine import SE_SUCCESS, SE_BAD_REQUEST, SE_CONFLICT, SE_CREATED
from shipengine import SE_INTERNAL, SE_MULTI_STATUS, SE_NO_CONTENT
from shipengine import SE_NOT_ALLOWED, SE_NOT_FOUND, SE_UNAUTHORIZED
from contextlib import contextmanager
import vcr
import pytest
from pprint import pprint

@pytest.fixture
def sut():
    return Download()

@pytest.fixture
def label_download_url():
    labeljson = {
        "shipment": {
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
        }
    }
    se = ShipEngine()
    r = se.post(url=se.url+"/v1/labels",json=labeljson)
    assert r.status_code == SE_SUCCESS
    return r.json()['label_download']['pdf']

@pytest.fixture
def label_download_endpoint(label_download_url):
    return label_download_url.replace("https://api.shipengine.com/v1/downloads",'')

@contextmanager
def does_not_raise():
    yield

@vcr.use_cassette('tests/vcr_cassettes/Download/download_file.yml', 
                    filter_query_parameters=['api_key'], 
                    filter_headers=['API-Key'])
@pytest.mark.parametrize(
    "test_value, expectation",
    [
        ("", pytest.raises(ImproperDownloadParameter)),
        ("/dir/subdir1/subdir2/filename", pytest.raises(ImproperDownloadParameter)),
        ("/dir/subdir/filename", pytest.raises(FileNotFound404)),
        (label_download_endpoint, does_not_raise())
    ],
)
def test_download_file(sut, test_value, expectation):
    
    with expectation:
        assert sut.download_file(filespec=test_value) is not None

@vcr.use_cassette('tests/vcr_cassettes/Download/download_url.yml', 
                    filter_query_parameters=['api_key'], 
                    filter_headers=['API-Key'])
@pytest.mark.parametrize(
    "test_value, expectation",
    [
        ("", pytest.raises(ImproperDownloadParameter)),
        ("https://api.shipengine.com/v1/downloads/dir/subdir1/subdir2/filename", pytest.raises(ImproperDownloadParameter)),
        ("https://api.shipengine.com/v1/downloads/dir/subdir/filename", pytest.raises(FileNotFound404)),
        (label_download_url, does_not_raise())
    ],
)
def test_download_url(sut, test_value, expectation):
    
    with expectation:
        assert sut.download_url(url=test_value) is not None

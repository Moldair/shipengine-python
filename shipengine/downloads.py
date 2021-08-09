from os import read, readlink
from posixpath import split
from shipengine import SE_BAD_REQUEST, SE_NOT_FOUND, SE_SUCCESS, ShipEngine
from shipengine import ImproperDownloadParameter,FileNotFound404
from pprint import pprint


class Download(ShipEngine):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _check_response(self):
        if self.response.status_code == SE_SUCCESS:
                self._file = self.response.text
                return True
        elif self.response.status_code == SE_BAD_REQUEST:
            raise FileNotFound404
        elif self.response.status_code == SE_NOT_FOUND:
            raise FileNotFound404
        
    def _get_file(self, filespec=None):
        _endpoint = "/v1/downloads"
        split_filespec = filespec.split('/')
        if split_filespec[0] == "":
            split_filespec = split_filespec[1:]
        if len(split_filespec) == 3:
            filespec = "/" + "/".join(split_filespec)
        else:
            raise ImproperDownloadParameter("download parameter should be of form /dir/subdir/filename")
        self.response = self.get(url=self.url+_endpoint+filespec)

    def download_url(self, url=None):
        _endpoint = "https://api.shipengine.com/v1/downloads"
        if isinstance(url, str):
            if _endpoint not in url:
                raise ImproperDownloadParameter
            filespec = url.replace(_endpoint, '')
            self._get_file(filespec)
            return self._check_response()
        return False

    def download_file(self, filespec=None):
        if isinstance(filespec, str):
            self._get_file(filespec)
            return self._check_response()
        return False

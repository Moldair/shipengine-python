from os import read, readlink
from posixpath import split
from shipengine import SE_BAD_REQUEST, SE_NOT_FOUND, SE_SUCCESS, ShipEngine
from pprint import pprint

class ImproperDownloadParameter(Exception):
    pass

class FileNotFound404(Exception):
    pass

class Download(ShipEngine):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def download_url(self, url=None):
        _endpoint = "/v1/downloads"
        if isinstance(url, str):
            if "https://api.shipengine.com/v1/downloads" not in url:
                raise ImproperDownloadParameter
            filespec = url.replace(self.url+_endpoint, '')
            split_filespec = filespec.split('/')
            if split_filespec[0] == "":
                split_filespec = split_filespec[1:]

            pprint(split_filespec)
            if len(split_filespec) == 3:
                filespec = "/" + "/".join(split_filespec)
            else:
                raise ImproperDownloadParameter("download parameter should be of form /dir/subdir/filename")


            self.response = self.get(url=self.url+_endpoint+filespec)
            pprint(self.response.json())
            if self.response.status_code == SE_SUCCESS:
                self._file = self.response.text
                return True
            elif self.response.status_code == SE_BAD_REQUEST:
                raise FileNotFound404
            elif self.response.status_code == SE_NOT_FOUND:
                raise FileNotFound404
        return False

    def download_file(self, filespec=None):
        _endpoint = "/v1/downloads"
        if isinstance(filespec, str):
            split_filespec = filespec.split('/')
            if split_filespec[0] == "":
                split_filespec = split_filespec[1:]

            pprint(split_filespec)
            if len(split_filespec) == 3:
                filespec = "/" + "/".join(split_filespec)
            else:
                raise ImproperDownloadParameter("download parameter should be of form /dir/subdir/filename")

            self.response = self.get(url=self.url+_endpoint+filespec)
            # pprint(self.response.status_code)
            # pprint(filespec)
            # pprint(self.url+_endpoint+filespec)
            # pprint(self.response.text)
            if self.response.status_code == SE_SUCCESS:
                self._file = self.response.text
                return True
            elif self.response.status_code == SE_BAD_REQUEST:
                raise FileNotFound404
            elif self.response.status_code == SE_NOT_FOUND:
                raise FileNotFound404
        return False

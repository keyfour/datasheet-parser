import validators
import os, http.cookiejar, urllib.request

class PDFDownloader:

    def __init__(self, url):
        self._url = None
        if isinstance(url, list):
            for u in url:
                if not validators.url(u):
                    url.remove(u)
            if len(url) > 0:
                self._url = url
        elif validators.url(url):
            self._url = url

        self._header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}


    def _download(self, url, path="/tmp/"):
        if url is not None:
            filename = url.split('/')[-1]
            print("Downloading {0} to {1}...".format(filename, path))
            r = None
            req = urllib.request.Request(url, headers=self._header)
            try:
                r = urllib.request.urlopen(req, timeout=10)
            except urllib.error.HTTPError as e:
                print(e)
            if not r:
                return
            print("Server response: {0}".format(r.status))
            if r.status == 200:
                file = path + filename
                with open(file, "wb") as f:
                    size = f.write(r.read())
                    print("Written {0}, {1} bytes".format(file, size))
    
    def download(self, path="/tmp/"):
        if isinstance(self._url, list):
            for l in self._url:
                self._download(l)
        else:
            self._download(self._url)

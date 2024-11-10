def gettimestamp(self):
    return self._request('GET', f'/timestamp')
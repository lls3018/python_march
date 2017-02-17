import json
import urllib2


def http_request(url, data=None, method='PUT',
                 headers=None, timeout=None, should_fail=False):
    headers = headers or {}
    request = urllib2.Request(url, data=data, headers=headers)
    request.get_method = lambda: method
    try:
        if timeout:
            return urllib2.urlopen(request, timeout=timeout)
        return urllib2.urlopen(request)
    except urllib2.URLError as e:
        if not should_fail:
            print('Failed to {0} {1} (reason: {2})'.format(
                method, url, e.reason))


headers_content = {
        "Content-Type": 'application/json'
    }

data_content = json.dumps({
    "force": "true",
})

endpoint = "http://192.168.84.32/api/v2/plugins/75e0f2b3-0640-48a3-82ce-e2e8874dc18a"


http_request(url=endpoint, headers=headers_content, data=data_content, method='DELETE')
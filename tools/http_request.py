from os.path import join, dirname
import urllib2
import json
import base64


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


def configure_grafana(host, port):
    print('Configuring Grafana Server...')
    endpoint = 'http://{0}:{1}/api/datasources'.format(host, port)
    datasource_url = 'http://192.168.84.22' + ':' + str(9200)
    grafana_hostStat = json.dumps({
        "name": "hostStat",
        "type": "elasticsearch",
        "url": datasource_url,
        "access": "proxy",
        "basicAuth": False,
        "database": "[qiqi-]YYYY.MM.DD",
        "jsonData": {
            "esVersion": 1,
            "interval": "Daily",
            "timeField": "@timestamp"
        }
    })

    auth = base64.b64encode('%s:%s' % ('admin', 'admin'))
    headers_content = {
        "Authorization": "Basic {0}".format(auth),
        "Content-Type": 'application/json'
    }

    http_request(url=endpoint, headers=headers_content, data=grafana_hostStat, method='POST')

configure_grafana('192.168.84.22', 3000)
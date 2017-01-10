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


def configure_grafana(grafana_server='localhost', grafana_port=80,
                      es_server='localhost', es_port=9200):
    print('Configuring Grafana Server...')
    endpoint = 'http://{0}:{1}/grafana/api/datasources'.format(grafana_server, grafana_port)
    datasource_url = 'http://{0}:{1}'.format(es_server, es_port)
    grafana_monitoring_host = json.dumps({
        "name": "hostmonitoring",
        "type": "elasticsearch",
        "url": datasource_url,
        "access": "proxy",
        "basicAuth": False,
        "database": "[smartcmp_monitoring_host-]YYYY.MM.DD",
        "jsonData": {
            "esVersion": 1,
            "interval": "Daily",
            "timeField": "@timestamp"
        }
    })

    grafana_monitoring_app = json.dumps({
        "name": "appmonitoring",
        "type": "elasticsearch",
        "url": datasource_url,
        "access": "proxy",
        "basicAuth": False,
        "database": "[smartcmp_monitoring_app-]YYYY.MM.DD",
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

    http_request(url=endpoint, headers=headers_content, data=grafana_monitoring_host, method='POST')
    http_request(url=endpoint, headers=headers_content, data=grafana_monitoring_app, method='POST')

configure_grafana(grafana_server='192.168.84.23', grafana_port=80, es_server='192.168.84.23', es_port=9200)
# -*- coding: utf-8 -*-
import urllib
from urlparse import urlparse

import httplib2


class HtmlJumping(object):
    @staticmethod
    def _get_connection(proxy_info):
        http_connection = None
        if proxy_info:
            import socks
            httplib2.debuglevel = 4
            http_connection = httplib2.Http(
                proxy_info = httplib2.ProxyInfo(socks.PROXY_TYPE_HTTP, proxy_info["host"], proxy_info["port"])
            )
        else:
            http_connection = httplib2.Http()
        return http_connection
    
    @staticmethod
    def _get_cookies(headers):
        cookies = None
        if 'set-cookie' in [key.lower() for key in headers.keys()]:
            cookies = headers.get('Set-cookie')
        return cookies
    
    @staticmethod
    def _set_header(headers, key, value):
        if value:
            headers[key] = value

    def _set_headers(self, headers, to_add_headers):
        for key, value in to_add_headers.iteritems():
            self._set_header(headers, key, value)
    
    @staticmethod
    def _set_referer(headers):
        if headers.get('Referer'):
            headers['Referer'] = headers.get('Referer')
    
    @staticmethod
    def _prepare_get_url_with_body(url, body):
        parsed_url = urlparse(url)
        if not parsed_url.query:
            url += "?%s" % urllib.urlencode(body)
        else:
            url += "&%s" % urllib.urlencode(body)
        return url

    @staticmethod
    def _check_url_info_required_parameters(url_info):
        if not ('url' in url_info and 'method' in url_info):
            raise Exception("url and method must be defined in each url_info to retrieve")
    
    def get(self, urls, permanent_headers = {}, proxy_info = None):
        http_connection = self._get_connection(proxy_info)
        url = None
        cookies = None
        for url_info in urls:
            headers = {}
            self._set_headers(headers, permanent_headers)
            self._set_header(headers, 'Cookie', cookies)
            self._set_header(headers, 'Referer', url)
            self._check_url_info_required_parameters(url_info)
            if 'body' in url_info:
                headers['Content-Type'] = 'application/x-www-form-urlencoded'
                if url_info['method'] == "GET":
                    base_url = self._prepare_get_url_with_body(url_info['url'], url_info['body'])
                    response, content = http_connection.request(base_url, url_info['method'], headers=headers)
                else:
                    response, content = http_connection.request(
                        url_info['url'],
                        url_info['method'],
                        headers=headers,
                        body=urllib.urlencode(url_info['body'])
                    )
            else:
                response, content = http_connection.request(url_info['url'], url_info['method'], headers=headers)
            cookies = self._get_cookies(headers)
            url = url_info['url']
        return response, content

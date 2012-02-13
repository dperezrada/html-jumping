# -*- coding: utf-8 -*-
import urllib
from urlparse import urlparse
from copy import deepcopy

import httplib2


class HtmlJumping(object):
    def __init__(self, proxy_info = None):
        self.http_connection = self._get_connection(proxy_info)
        self.headers = {}
    
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
        cookies = ""
        keys = filter(lambda el: el[1] == 'set-cookie', [(key, key.lower()) for key in headers.keys()])
        if len(keys) >0:
            cookies = headers.get(keys[0][1])
        final_cookies = ""
        for cookie in cookies.split(','):
            cookie = cookie.split(';')[0].strip()
            if cookie.strip():
                final_cookies += cookie +"; "
        return final_cookies
    
    @staticmethod
    def _set_header(headers, key, value, append = False):
        if value:
            if append:
                headers[key] = headers.get(key, '') + value
            else:
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

    def request(self, url, method = 'GET', body = None, headers = {}):
        request_headers = deepcopy(headers)
        self._set_headers(request_headers, self.headers)
        if body:
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
            if method == 'GET':
                base_url = self._prepare_get_url_with_body(url, body)
                response, content = self.http_connection.request(base_url, method, headers=request_headers)
            else:
                response, content = self.http_connection.request(
                    url,
                    method,
                    headers=request_headers,
                    body=urllib.urlencode(body)
                )
        else:
            response, content = self.http_connection.request(url, method, headers=request_headers)
        self._set_header(self.headers, 'Cookie', self._get_cookies(response), append = True)
        self._set_header(self.headers, 'Referer', url)
        return response, content
    
    def get(self, urls, permanent_headers = {}, proxy_info = None):
        for url_info in urls:
            headers = url_info.get('headers', {})
            self._set_headers(headers, permanent_headers)
            self._check_url_info_required_parameters(url_info)
            response, content = self.request(url_info.get('url'), url_info.get('method'), url_info.get('body'), headers)
        return response, content

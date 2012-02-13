# encoding: utf-8
import os
from unittest import TestCase
from html_jumping import HtmlJumping
from lxml import etree
from StringIO import StringIO

class TestHTMLJumping(TestCase):
    def setUp(self):
        self.handler = HtmlJumping()
        
    def test_get_html_jumping(self):      
        urls_config = [
            {
                'url': 'http://pypi.python.org/pypi',
                'method': 'GET'
            },
            {
                'url': 'http://pypi.python.org/pypi',
                'method': 'GET',
                'body': {
                    'term': 'html_jumping',
                    ':action': 'search',
                    'submit': 'search'
                }
            }
        ]
        received_header, received_content = self.handler.get(urls_config)
        parser = etree.HTMLParser()
        tree   = etree.parse(StringIO(received_content), parser)
        
        h1_title = tree.xpath('//div[@class="section"]/h1/text()')[0]
        self.assertEqual('html_jumping', h1_title.split(" ")[0])

    def test_remember_headers(self):
        urls_config = [
            {
                'url': 'http://pypi.python.org/pypi',
                'method': 'GET'
            }
        ]
        received_header, received_content = self.handler.get(urls_config)
        self.assertEqual({'Referer': 'http://pypi.python.org/pypi'}, self.handler.headers)
    
    def test_remember_headers_in_get(self):
        urls_config = [
            {
                'url': 'http://pypi.python.org/pypi',
                'method': 'GET'
            }
        ]
        received_header, received_content = self.handler.get(urls_config)
        self.assertEqual({'Referer': 'http://pypi.python.org/pypi'}, self.handler.headers)

    def test_remember_headers_in_request(self):
        urls_config = [
            {
                'url': 'http://pypi.python.org/pypi',
                'method': 'GET'
            }
        ]
        received_header, received_content = self.handler.get(urls_config)
        self.handler.request('http://pypi.python.org/pypi/html_jumping')
        self.assertEqual({'Referer': 'http://pypi.python.org/pypi/html_jumping'}, self.handler.headers)
    
    def test_get_cookies(self):
        headers = {'set-cookie': 'IdUsuarioASP=; path=/, ASPSESSIONIDCCTSTRDB=DGCFHJCAGLAEMENHGMMEBLGG; path=/'}
        self.assertEqual('IdUsuarioASP=; ASPSESSIONIDCCTSTRDB=DGCFHJCAGLAEMENHGMMEBLGG; ', self.handler._get_cookies(headers))
    
    def test_set_cookies(self):
        headers = {'cookie': 'IdUsuarioASP=;'}
        self.handler._set_header(headers, 'cookie', 'ASPSESSIONIDCCTSTRDB=DGCFHJCAGLAEMENHGMMEBLGG;', True)
        self.assertEqual('IdUsuarioASP=;ASPSESSIONIDCCTSTRDB=DGCFHJCAGLAEMENHGMMEBLGG;', headers['cookie'])
        
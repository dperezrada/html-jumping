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
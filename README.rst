.. -*- mode: rst; coding: utf-8 -*-

Welcome to HTML-Jumping
=======================

:Author: * Daniel Perez Rada <@dperezrada>

What?
=====
Allows to get an HTML, coming from several previous URLs. Sometimes this is needed to get webpages that requires cookies or a HTTP referrer to get a certain page.

Pre-requisites
==============
You will need:

* httplib2
* http://socksipy.sourceforge.net/ (if you want to use a proxy)

To run the test you will also need:

* lxml

Example
=======
No proxy
--------
::

    from html_jumping import HtmlJumping
    handler = HtmlJumping()
    urls = [
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
    received_header, received_content = handler.get(urls)

With proxy
----------
Allow you to use a HTTP proxy, you will need to install the socksipy library.
::

    from html_jumping import HtmlJumping
    handler = HtmlJumping()
    urls = [
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
    received_header, received_content = handler.get(
        urls,
        proxy_info = {'host': '127.0.0.1', 'port': '8081'}
    )


With permanent headers
----------------------
This will sent in each call the headers 'Accept-Language'.
::

    from html_jumping import HtmlJumping
    handler = HtmlJumping()
    urls = [
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
    received_header, received_content = handler.get(
        urls,
        permanent_headers = {'Accept-Language': 'es, en-cl;q=0.5'}
    )

Tests
=====

Run
---

    >> nosetests

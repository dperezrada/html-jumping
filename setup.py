# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
  name = "html_jumping",
  version = "0.2.2",
  author = "Daniel Perez Rada",
  author_email = "dperezrada@gmail.com",
  description = ("Allows to get an HTML, coming from several previous URLs. Sometimes this is needed to get webpages that requires cookies or a HTTP referrer to get a certain page."),
  license='GNU Public License v3.0',
  keywords = "html_jumping cookies html get post form referrer",
  url = "https://github.com/dperezrada/html_jumping",
  packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
  long_description=read('README.rst'),
  classifiers=[
      "Development Status :: 3 - Alpha",
      "Topic :: Utilities",
      "Intended Audience :: Developers",
      "License :: OSI Approved :: GNU General Public License (GPL)",
  ],
  install_requires=[
        "httplib2"
    ],
)

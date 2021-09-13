#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: cloudformation.py
#
# Copyright 2021 Costas Tyfoxylos
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
#

"""
Main code for billing.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import logging

from awsapilib.authentication import Authenticator, LoggerMixin

__author__ = '''Costas Tyfoxylos <ctyfoxylos@schubergphilis.com>'''
__docformat__ = '''google'''
__date__ = '''13-09-2021'''
__copyright__ = '''Copyright 2021, Costas Tyfoxylos'''
__credits__ = ["Costas Tyfoxylos"]
__license__ = '''MIT'''
__maintainer__ = '''Costas Tyfoxylos'''
__email__ = '''<ctyfoxylos@schubergphilis.com>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".

# This is the main prefix used for logging
LOGGER_BASENAME = '''cloudformation'''
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())


class Cloudformation(LoggerMixin):  # pylint: disable=too-few-public-methods
    """Models Control Tower by wrapping around service catalog."""

    def __init__(self, arn, region=None):
        self.aws_authenticator = Authenticator(arn)
        self.session = self._get_authenticated_session()
        self.region = region or self.aws_authenticator.region

    def _get_authenticated_session(self):
        return self.aws_authenticator.get_cloudformation_authenticated_session()

    @property
    def stacksets(self):
        return StackSet(self)


class StackSet:

    def __init__(self, cloudformation_instance):
        self._cloudformation = cloudformation_instance
        self._api_url = (f'{cloudformation_instance.aws_authenticator.urls.regional_console}/'
                         f'cloudformation/service/stacksets/')

    @property
    def organizations_trusted_access(self):
        endpoint = 'describeOrganizationsTrustedAccess'
        payload = {'region': self._cloudformation.aws_authenticator.region}
        response = self._cloudformation.session.get(f'{self._api_url}/{endpoint}', params=payload)
        if not response.ok:
            raise ValueError(f'Error, response received : {response.text}')
        return response.json().get('status') == 'ENABLED'
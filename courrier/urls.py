#!/usr/bin/env python
# -*- coding: utf-8 -*-
##
## Author: Adriano Marques <adriano@umitproject.org>
##
## Copyright (C) 2012 S2S Network Consultoria e Tecnologia da Informacao LTDA
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU Affero General Public License as
## published by the Free Software Foundation, either version 3 of the
## License, or (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Affero General Public License for more details.
##
## You should have received a copy of the GNU Affero General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.
##

from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('courrier.views',
                       url(r'^courrier/run_tests/?$', "run_tests"),
                       url(r'^courrier/bulk_populate/?$', "bulk_populate"),
                       url(r'^_ah/mail/test_suite@the-courrier.appspotmail.com/?$', "inbound_test_suite_email"),
                       url(r'^_ah/mail/(?P<email>.*)/?$', "inbound_email"),
                       
                       # URL calls from customers
                       url(r'^send_email/?$', "send_email"),
                       
                       # CRON
                       url(r'^courrier/cron/send_email$', 'cron_send_email'),
)

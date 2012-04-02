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

import logging

from django.shortcuts import render_to_response
from django.template.loader import render_to_string

from django.http import Http404, HttpResponse
from django.core.paginator import Paginator
from django.utils import translation

from django.db import models
from django.core.cache import cache

from courrier.core import add_email as core_add_email


def add_email(request):
    """This is the external interface for customers to register e-mails into
    our datastore.
    """
    return render_to_response(request, "courrier/add_email.html", locals())

def send_email(request):
    return render_to_response(request, "courrier/send_email.html", locals())

def send_bulk_email(request):
    return render_to_response(request, "courrier/send_bulk_email.html", locals())

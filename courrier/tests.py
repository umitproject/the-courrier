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

import unittest
import random
import datetime
import logging
import re

from time import time
from courrier.models import *
from courrier.views import *

from django.test.client import Client


class TestCourrier(unittest.TestCase):
    def setUp(self):
        self.test_customer = Customer(name="Test Customer",
                                      email="customer@test.com",
                                      website="http://www.test.com",
                                      phone="+55 62 7689 8777",
                                      mobile="+55 62 9978 4231",
                                      contact_name="Godzilla Spring",
                                      country="Brazil",
                                      language="Portuguese")
        self.test_customer.save()

        self.test_campaign = Campaign(name="Invasion Alert Campaign",
                                               description="Alien invasion alert "
                                               "to all subscribers of our site.",
                                               customer=self.test_customer.pk,
                                               group_list=["alien"],
                                               html_template="""
                                               """,
                                               text_template="""
                                               """,
                                               link="http://www.test.com",
                                               sender_email="test_robot@thecourrier.appspotmail.com",
                                               sender_name="Test Robot",
                                               reply_to_email="test_robot@thecourrier.appspotmail.com",
                                               reply_to_name="Test Robot",
                                               subject="Welcome to Test Network")
        self.test_campaign.save()
        
        self.test_email = Email(first_name="Godzilla",
                                middle_name="Monster",
                                last_name="Spring",
                                email="test_suite@thecourrier.appspotmail.com",
                                birthday=datetime.datetime(1968, 8, 24, 9, 50),
                                gender="Male",
                                twitter="test",
                                facebook="test",
                                website="http://www.test.com",
                                language="English",
                                country="Brazil",
                                city="Rio de Janeiro",
                                added_from="Test Suite",
                                customers=[self.test_customer.pk],
                                campaigns=[self.test_campaign.pk],
                                group_list=["test"])
        self.test_email.save()

    def tearDown(self):
        self.test_customer.delete()
        self.test_campaign.delete()
        self.test_email.delete()
    
    def _create_send_email_entity(self):
        self.test_send_email = SendEmail(customer=self.test_customer.pk,
                                         campaign=self.test_campaign.pk,
                                         sender_email=self.test_campaign.sender_email,
                                         sender_name=self.test_campaign.sender_name,
                                         reply_to_email=self.test_campaign.reply_to_email,
                                         reply_to_name=self.test_campaign.reply_to_name,
                                         subject=self.test_campaign.subject,
                                         html_template=self.test_campaign.html_template,
                                         text_template=self.test_campaign.text_template,
                                         email_key=self.test_email.pk,
                                         email=self.test_email.email)
        self.test_send_email.save()
        self.test_send_email.subject = "%s - %s" % (self.test_send_email.subject,
                                                    self.test_send_email.pk)
        self.test_send_email.save()

    def testCronSendEmail(self):
        """Test to verify if cron is actually sending the emails
        """
        self._create_send_email_entity()
        
        response = Client().get("/courrier/cron/send_email")
        self.assertEqual(response.status_code, 200)
        
        income = SendEmail.objects.get(subject=self.test_send_email.subject)
        self.assertNotEqual(income, None)
        
        self.test_send_email.delete()


if __name__ == "__main__":
    unittest.main()



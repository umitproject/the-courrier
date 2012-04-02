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

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.db.models.signals import post_save, pre_save
from dbextra.fields import ListField

GENDERS = ["Male", "Female", "Undefined"]
LANGUAGES = ["Portuguese", "English", "Spanish", "French", "Dutch", "German", "Undefined"]
COUNTRIES = ["Brazil",
             "United States",
             "Mexico",
             "Spain",
             "France",
             "Belgium",
             "Netherlands",
             "Luxembourg",
             "United Kingdom",
             "Undefined"]
ADDED_FROM = ["Initial Populate",
              "Customer Bulk Submission",
              "Customer Submission",
              "Customer Sending Email",
              "Customer Sending Bulk Email",
              "Own Bulk Submission",
              "Test Suite"]
MIME_TYPES = ["application/msword",
              "application/pdf",
              "application/rss+xml",
              "application/vnd.ms-excel",
              "application/vnd.ms-powerpoint",
              "application/vnd.oasis.opendocument.presentation",
              "application/vnd.oasis.opendocument.spreadsheet",
              "application/vnd.oasis.opendocument.text",
              "application/vnd.sun.xml.calc",
              "application/vnd.sun.xml.writer",
              "audio/basic",
              "audio/flac",
              "audio/mid",
              "audio/mp4",
              "audio/mpeg",
              "audio/ogg",
              "audio/x-aiff",
              "audio/x-wav",
              "image/gif",
              "image/jpeg",
              "image/png",
              "image/tiff",
              "image/vnd.wap.wbmp",
              "image/x-ms-bmp",
              "text/calendar",
              "text/comma-separated-values",
              "text/css",
              "text/html",
              "text/plain",
              "text/x-vcard",
              "video/mp4",
              "video/mpeg",
              "video/ogg",
              "video/quicktime",
              "video/x-msvideo"]
MAX_EMAIL_SEND_ATTEMPTS = 3

class Customer(models.Model):
    """
    The Customer object represents an entity that uses the system to send
    out notifications/emails using the campaigns it can create.
    """
    name = models.CharField(max_length=255)
    email = models.EmailField()
    website = models.URLField()
    phone = models.CharField(max_length=30)
    mobile = models.CharField(max_length=30)
    contact_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)
    country = models.CharField(max_length=100, choices=COUNTRIES)
    language = models.CharField(max_length=100, choices=LANGUAGES)

class Campaign(models.Model):
    """
    A Campaign is a type of email that a customer can send. The campaign
    defines its own templates and sending properties.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    customer = models.IntegerField()
    group_list = ListField()
    html_template = models.TextField()
    text_template = models.TextField()
    link = models.URLField()
    sender_email = models.EmailField()
    sender_name = models.CharField(max_length=255)
    reply_to_email = models.EmailField()
    reply_to_name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)


class SendEmail(models.Model):
    """
    This entity register an email sending task, and records any failed
    attempts and retries.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    customer = models.IntegerField()
    campaign = models.IntegerField()
    sender_email = models.EmailField()
    sender_name = models.CharField(max_length=255, default="")
    reply_to_email = models.EmailField()
    reply_to_name = models.CharField(max_length=255, default="")
    subject = models.CharField(max_length=255)
    html_template = models.TextField(default="")
    text_template = models.TextField(default="")
    email_key = models.CharField(max_length=255) # Email's key
    email = models.EmailField()
    sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField() # date and time when it was sent
    attempts = models.IntegerField(default=0) # number of attempts
    logs = models.TextField(default="") # Log whatever errors we get while attempting
    
    def __unicode__(self):
        return "%s - Sent %s - Attempts %s" % (self.email, self.sent, self.attempts)


class IncomeEmail(models.Model):
    """
    This entity stores any income email received for later processing.
    """
    received_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    recipient = models.EmailField()
    sender = models.EmailField()
    attachments = ListField()
    subject = models.CharField(max_length=255, default="")
    body = models.TextField(default="")
    

class Attachment(models.Model):
    """
    Attachment entity. Relates to an income email.
    """
    received_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    income_email = models.IntegerField()
    content_type = models.CharField(max_length=100, choices=MIME_TYPES)
    attachment = models.FileField()


class Email(models.Model):
    """

    """
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    birthday = models.DateTimeField()
    gender = models.CharField(max_length=10, choices=GENDERS, default="Undefined")
    twitter = models.CharField(max_length=100)
    facebook = models.CharField(max_length=255)
    website = models.URLField()
    language = models.CharField(max_length=100, choices=LANGUAGES, default="Undefined")
    country = models.CharField(max_length=100, echoices=COUNTRIES, default="Undefined")
    city = models.CharField(max_length=255)
    added_from = models.CharField(max_length=255, choices=ADDED_FROM)
    customers = ListField(py_type=int)
    campaigns = ListField(py_type=int)
    group_list = ListField(py_type=int)
    valid = models.BooleanField(default=True)
    logs = models.TextField(default="")
    reads = models.IntegerField(default=0)
    responses = models.IntegerField(default=0)
    unsubscribed = models.BooleanField(default=False)
    unsubscribed_at = models.BooleanField(required=False)
    
    def __unicode__(self):
        return '<%s> %s - %s' % ('%s %s %s' % (self.first_name,
                                               self.middle_name,
                                               self.last_name),
                                 self.email, self.added_from)


class EmailGroup(models.Model):
    """In order to make things faster while sending bulk emails, we may want
    to aggregate emails into groups. Each entity of this model may contain up
    to 1Mb of emails. If we need a group bigger than that, then we need to
    create more than one entity.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    group = models.IntegerField()
    description = models.CharField(max_length=255, default="")
    emails = ListField()
    next_in_group = models.IntegerField()
    first_in_group = models.BooleanField(default=False)


# TODO: We need to take a daily snapshot of the values in this aggregation
class GlobalCourrierAggregation(models.Model):
    aggregated_at = models.DateTimeField(auto_now=True)
    total_accesses = models.IntegerField(default=0)
    total_unique_accesses = models.IntegerField(default=0)
    total_emails = models.IntegerField(default=0)
    total_subscriptions = models.IntegerField(default=0)
    total_unsubscriptions = models.IntegerField(default=0)
    total_groups = models.IntegerField(default=0)
    total_emails_sent = models.IntegerField(default=0)
    total_emails_returned = models.IntegerField(default=0)
    valid_emails = models.IntegerField(default=0)
    invalid_emails = models.IntegerField(default=0)


###############################################################################
#
# With Google App Engine, we don't have an easy way of making aggregations
# on the fly. This is due to several quotas and app engine limitations that
# are imposed by Google. In order to overcome this, and still provide our
# users with the useful aggregated data, we need to make a pre-aggregation,
# or an aggregation on create, update or delete events of a model. This way,
# we always have the aggregation ready and handy.
#
###############################################################################

def post_aggregate_email(sender, instance, created, **kwargs):
    """When a subscriber instance is created, we add this info to the related
    aggregations, and add to the beta testers counter as well.
    """
    save_groups = []
    if created:
        global_courrier_aggregations.total_emails += 1
        global_courrier_aggregations.valid_emails += 1
        
        # TODO: Disabling email groups for now. Will work on this idea
        # later. Some questions on how to update/remove emails from this
        # list is already unclear and not strictly necessary for this first
        # release
        #for group in instance.group_list:
        #    g = EmailGroup.all().filter("group =", group).\
        #                         filter("first_in_group =", True).get()
        #    g.emails.append(instance.email)
        #    
        #    save_groups.append(g)
    
    [a.save for a in (save_groups + [global_courrier_aggregations])]

def pre_aggregate_email(sender, instance, **kwargs):
    try:
        old_instance = sender.objects.get(id=instance.pk)
    except db.NotSavedError, err:
        return
    else:
        if old_instance.valid and not instance.valid:
            global_courrier_aggregations.valid_emails -= 1
            global_courrier_aggregations.invalid_emails += 1
        
        global_courrier_aggregations.save()

def aggregate_groups(sender, instance, created, **kwargs):
    if created:
        pass

post_save.connect(post_aggregate_email, sender=Email)
pre_save.connect(pre_aggregate_email, sender=Email)
#post_save.connect(aggregate_groups, sender=EmailGroup)


###############################################################################
# Setting up the Global Courrier Aggregation instance
global_courrier_aggregations = None

gca = GlobalCourrierAggregation.objects.all()
if not gca:
    global_courrier_aggregations = GlobalCourrierAggregation()
    global_courrier_aggregations.save()
else:
    global_courrier_aggregations = gca[0]




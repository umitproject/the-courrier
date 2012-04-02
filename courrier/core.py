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

from django.template import Context, Template
from django.db import models

from courrier.models import Customer, Campaign, Email, SendEmail


def add_email():
    """This method is responsible for adding emails to the datastore. But,
    before actually adding, we must verify if the email already exist in
    the datastore for the given customer/campaign. If it doesn't, then
    we create a new record. If it does exist and is linked to that customer,
    then we update the records with whatever new info we got from that user
    during this add. If it does exist, but is linked to another customer, then
    we update both with the most up to date info.
    Finally, we return the new or updated record.
    """
    pass


def send_email(email, campaign, context={}):
    """This function is used to send individual emails. Don't use this for
    bulk sending, as it is more expensive. Please, use send_bulk_email
    instead.
    
    @type email: dictionary
    @param email: The email and its owner's data to be stored in the datastore
    @type campaign: string
    @param campaign: A string with campaign's key
    
    @rtype: tuple
    @return: A tuple, with a boolean in the first position, and a list in
             the second one. True if successfully added and scheduled for
             sending or False in case something went wrong in the first
             position, and a list of strings containing all error or info
             messages produced during the procedure.
    
    # TODO: Must be able to receive the html, text, html_template, text_template
    # and create the content on the fly. Must also be able to send without a
    # campaign, using only the customer_key
    """
    success = True
    msg = []
    campaign_obj = None
    customer_obj = None
    customer = ""
    
    email_addr = email.get("email", None)
    if email_addr is None:
        msg.append("The email field is required!")
        success = False
    
    # Validate customer and campaign keys
    try:
        campaign_obj = Campaign.objects.get(pk=campaign)
    except Exception, err:
        success = False
        msg.append("Couldn't validate campaign! '%s'" % str(campaign))
        msg.append(str(err))
    else:
        msg.append("Campaign validated.")
    
    try:
        customer_obj = Customer.objects.get(pk=campaign_obj.customer)
    except Exception, err:
        success = False
        msg.append("Couldn't validate customer!")
        msg.append(str(err))
    else:
        customer = str(customer_obj.key())
        msg.append("Customer validated.")
    
    if not success:
        # Get out if failed any of the steps above
        return success, msg
    
    if not email.has_key("added_from"):
        email["added_from"] = "Customer Sending Email"
    
    new_email = False
    email_obj = Email.objects.get(email=email_addr)
    if email_obj is None:
        msg.append("Created an entry for this email.")
        email_obj = Email(**email)
        new_email = True
    else:
        msg.append("Found an entry for this email.")
    
    email_obj = _update_email_entry(email_obj, email) 
    
    for c in email_obj.customers:
        if c == customer:
            msg.append("Customer already owns this email entry.")
            break
    else:
        msg.append("Assigned email entry to customer.")
        email_obj.customers.append(customer)
    
    for c in email_obj.campaigns:
        if c == campaign:
            msg.append("Campaign already owns this email entry.")
            break
    else:
        msg.append("Assigned email entry to campaign.")
        email_obj.campaigns.append(str(campaign))
    
    # TODO: put this inside a try/except and handle accordingly to avoid losing
    email_obj.save()
    
    # Now, schedule the email to send!
    send_email = _schedule_email(campaign_obj, email_obj, context=context)
    
    # TODO: put this inside a try/except and handle accordingly to avoid losing
    send_email.save()
    
    return success, msg

def _schedule_email(campaign, email, context={}, save=False):
    """This function will create a SendEmail entry to send the email.
    
    @type campaign: Campaign
    @param campaign: Campaign entity in the datastore
    @type email: Email
    @param email: Email entity in the datastore
    @type save: Boolean
    @param save: If the SendMail instance should be saved or not
    @rtype: SendEmail
    @return: a SendEmail instance
    """
    html_template = Template(campaign.html_template).render(Context(context))
    text_template = Template(campaign.text_template).render(Context(context))
    
    send_email = SendEmail(customer=campaign.customer,
                           campaign=str(campaign.key()),
                           sender_email=campaign.sender_email,
                           sender_name=campaign.sender_name,
                           reply_to_email=campaign.reply_to_email,
                           reply_to_name=campaign.reply_to_name,
                           subject=campaign.subject,
                           html_template=html_template,
                           text_template=text_template,
                           email_key=str(email.key()),
                           email=email.email)
    
    if save:
        send_email.save()
    
    return send_email


def _update_email_entry(email_obj, email_data, save=False):
    """
    
    @type email_obj: Email
    @param email_obj: The Email instance that must be updated
    @type email_data: dictionary
    @param email_data: A dictionary with keys being equivalent to the Email
                       instance's field names and the values as the values
                       that should be attributed to those fields in the
                       email_obj
    @type save: boolean
    @param save: A boolean on whether this instance should be saved after the
                 update or not. Default is False. Useful when we want to work
                 with the instance after the update and then save it.
    @rtype: Email
    @return: The updated email instance
    """
    
    
    if save:
        email_obj.save()
    
    return email_obj


def send_bulk_email():
    """This function is used to send bulk emails based (or not) on templates.
    If you want to send only one email, then please refer to send_email
    function instead.
    """
    pass










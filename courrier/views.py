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
import datetime

from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import Template

from django.http import Http404, HttpResponse
from django.core.paginator import Paginator
from django.utils import translation, simplejson as json

from google.appengine.runtime import apiproxy_errors

from google.appengine.api import mail

from courrier.models import *
from courrier.core import send_email
from courrier.forms import UnsubscribeForm


def home(request):
    return render_to_response(request, "courrier/home.html", locals())

def register_bulk_csv(request):
    return render_to_response(request, "courrier/register_bulk_csv.html", locals())

def subscribe(request):
    form = None
    
    if not request.POST:
        pass
    
    return render_to_response(request, "courrier/subscribe.html", locals())

def unsubscribe(request):
    form = None
    
    if not request.POST:
        form = UnsubscribeForm()
        
        return render_to_response(request, "courrier/unsubscribe.html", locals())
    else:
        form = UnsubscribeForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data['email']
            email = Email.objects.get(email=email)
            
            if email is not None:
                email.unsubscribed = True
                email.unsubscribed_at = datetime.datetime.today()
                email.save()
                
                return render_to_response(request, "courrier/unsubscribed.html", locals())
    
    return render_to_response(request, "courrier/unsubscribe.html", locals())

def view_mail(request):
    return render_to_response(request, "courrier/register_bulk_csv.html", locals())

def inbound_email(request, email):
    logging.error(email)
    return HttpResponse("OK")

def inbound_test_suite_email(request):
    return HttpResponse("OK")

def run_tests(request):
    from django.test.utils import setup_test_environment
    return HttpResponse(setup_test_environment())

def send_email(request):
    """This URL is available to call anytime, anywhere to send emails.
    """
    email_dict = dict(email=request.POST.get("email", None),
                      first_name=request.POST.get("first_name", None),
                      middle_name=request.POST.get("middle_name", None),
                      last_name=request.POST.get("last_name", None),
                      birthday=request.POST.get("birthday", None),
                      gender=request.POST.get("gender", None),
                      twitter=request.POST.get("twitter", None),
                      facebook=request.POST.get("facebook", None),
                      website=request.POST.get("website", None),
                      language=request.POST.get("language", None),
                      country=request.POST.get("country", None),
                      city=request.POST.get("city", None))
    
    result = core_send_email(email_dict,
                             request.POST.get("campaign", None))
    
    if result:
        return HttpResponse("OK")
    return HttpResponse("FAIL")

def cron_send_email(request):
    """This is a cron job that will be called every minute to go through the
    datastore records on model SendEmail and send email to each record found
    there.
    """
    emails = SendEmail.objects.filter(sent=False, attempts__lte=MAX_EMAIL_SEND_ATTEMPTS)[:10]
    save_emails = []
    
    for email in emails:
        try:
            html_template = Template(email.html_template)
            text_template = Template(email.text_template)
            context = email.__dict__
            
            mail.send_mail(sender="%s <%s>" % (email.sender_name,
                                               email.sender_email),
                           to=email.email,
                           subject=email.subject,
                           body=text_template.render(context),
                           reply_to="%s <%s>" % (email.reply_to_name,
                                                 email.reply_to_email),
                           html=html_template.render(context))
        except mail.InvalidSenderError, err:
            email.attempts += 1
            email.logs += "%s\n%s\n%s" % (80*"-", str(err), 80*"-")
            save_emails.append(email)
        except mail.InvalidEmailError, err:
            logging.error(err)
            email.attempts = 4 # Won't try again
            email.sent = False
            save_emails.append(email)
            
            email_obj = Email.get(email.email_key)
            email_obj.valid = False
            save_emails.append(email_obj)
            
            global_courrier_aggregations.invalid_emails += 1
        except mail.BadRequestError, err:
            email.attempts += 1
            email.logs += "%s\n%s\n%s" % (80*"-", str(err), 80*"-")
            save_emails.append(email)
        except mail.Error, err:
            logging.error(err)
            email.attempts += 1
            email.logs += "%s\n%s\n%s" % (80*"-", str(err), 80*"-")
            save_emails.append(email)
        except apiproxy_errors.OverQuotaError, err:
            logging.error(err)
            email.logs += "%s\n%s\n%s" % (80*"-", str(err), 80*"-")
        except Exception, err:
            # Possibly not a mail error, but a coding error somewhere.
            # This isn't considered an attempt in this case.
            logging.error(err)
            email.logs += "%s\n%s\n%s" % (80*"-", str(err), 80*"-")
            save_emails.append(email)
        else:
            global_courrier_aggregations.valid_emails += 1
            
            email.sent = True
            save_emails.append(email)
    
    save_emails.append(global_courrier_aggregations)
    [e.save() for e in save_emails]
    
    return HttpResponse("OK")

def bulk_populate(request):
    if request.POST:
        emails = json.loads(request.POST.get('emails', ''))
        if emails:
            counter = 0
            for email in emails:
                # Check if email is already in
                e = Email.objects.get(email=email[1])
                name = email[0].split(' ')
                first_name = ' '.join(name[:1] or '')
                middle_name = ' '.join(name[1:-1] or '')
                last_name = ' '.join(name[-1:] or '')
                
                if not e:
                    e = Email(first_name=first_name, middle_name=middle_name, last_name=last_name,
                              email=email[1],
                              added_from=ADDED_FROM[5])
                    counter += 1
                else:
                    if e.first_name == '':
                        e.first_name = first_name
                    if e.middle_name == '':
                        e.middle_name = middle_name
                    if e.last_name == '':
                        e.last_name = last_name
                    
                e.save()
            
            return HttpResponse("OK - %s" % counter)
    raise Http404
        
        
        
        
        
        
        
        

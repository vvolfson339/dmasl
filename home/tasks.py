from __future__ import absolute_import, unicode_literals
import random
from celery.decorators import task
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.shortcuts import get_object_or_404
import time
import datetime

from account import models as account_model


@task(name='send_member_add')
def send_member_add(member_id):
    #member = account_model.UserProfile.get(id=member_id)
    member = get_object_or_404(account_model.UserProfile, username=member_id)
    fromaddr = 'dmasl_enrolment@volfson.ca'
    #toaddr = ('test1@volfson.ca', 'test2@volfson.ca')
    toaddr = ('jonathan_aycan@dmasl.com','catherina_dawson@dmasl.com')

    password = 'sqesncowiwlikkik'

    msg = MIMEMultipart()

    msg['Subject'] = "New Member Added to {}".format(member.org.org_short_name)
    msg['From'] = fromaddr
    msg['To'] = ", ".join(toaddr)

    name = None

    if member.last_name:
        name = member.last_name

    if member.first_name:
        name += " " +member.first_name

    body = """
        <!html>
            <head>
                <style></style>
            </head>

            <body>

                <h2 style="margin-top: 30px;">New Member Detail:</h2>

                <p>Organization: {}</p>
                <p>UserID: {}</p>
                <p>Member Name: {}</p>
                <p>Effective Date: {}</p>
                <p>Date Added: {}</p>
                <p>Total Benefit Credits: {}</p>


            </body>
        </html>
        """.format(member.org.org_short_name, member.username, name, member.effective_date, member.join_date.strftime("%Y-%m-%d"), member.hsa_annual_credits)


    msg.attach(MIMEText(body, 'html'))


    smtpserver = smtplib.SMTP('smtp.gmail.com', 587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(fromaddr,password)

    smtpserver.sendmail(fromaddr,toaddr,msg.as_string())
    smtpserver.close()

@task(name='send_new_member_detail')
def send_new_member_detail(member_id):
    member = get_object_or_404(account_model.UserProfile, username=member_id)
    fromaddr = 'dmasl_enrolment@volfson.ca'
    #toaddr = ('test1@volfson.ca', 'test2@volfson.ca')
    toaddr = ('jonathan_aycan@dmasl.com','catherina_dawson@dmasl.com')

    password = 'sqesncowiwlikkik'

    msg = MIMEMultipart()

    msg['Subject'] = "New Member Enrolment Sumbission from {}".format(member.org.org_short_name)
    msg['From'] = fromaddr
    msg['To'] = ", ".join(toaddr)

    name = None

    if member.last_name:
        name = member.last_name

    if member.first_name:
        name += " " +member.first_name

    body = """
        <!html>
            <head>
                <style></style>
            </head>

            <body>

                <h2 style="margin-top: 30px;">Member Details:</h2>

                <p>Organization: {}</p>
                <p>UserID: {}</p>
                <p>Member Name: {}</p>
                <p>Effective Date: {}</p>
                <p>Date Added: {}</p>
                <p>Total Benefit Credits: {}</p>
                <p>Health Spending Account Selection: {}</p>
                <p>Benefit Credits Remaining: {}</p>



            </body>
        </html>
        """.format(member.org.org_short_name, member.username, name, member.effective_date, member.join_date.strftime("%Y-%m-%d"), member.hsa_annual_credits, member.hsa_optional, member.hsa_remaining)


    msg.attach(MIMEText(body, 'html'))


    smtpserver = smtplib.SMTP('smtp.gmail.com', 587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(fromaddr,password)

    smtpserver.sendmail(fromaddr,toaddr,msg.as_string())
    smtpserver.close()

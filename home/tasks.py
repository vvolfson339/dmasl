from __future__ import absolute_import, unicode_literals
import random
from celery.decorators import task
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import datetime

from account import models as account_model


@task(name='sent_hsa_detail_to_member')
def sent_hsa_detail_to_member(member_id, hsa_optional, new_hsa_remaining, salary_adjusted):
    member = account_model.UserProfile.objects.get(id=member_id)

    fromaddr = "dmasl_enrolment@volfson.ca"
    toaddr = member.email

    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr

    msg['Subject'] = "You just enroll HSA in dmasl"


    name = None

    if member.last_name:
        name = member.last_name

    if member.first_name:
        name += " " +member.first_name

    if member.middle_name:
        name += " " + member.middle_name

    body = """
        <!html>
            <head>
                <style></style>
            </head>
            
            <body>
                
                <h2>Your enrolment application details is below: </h2>
                
                <h3 style="margin-top: 30px;">Member detail</h3>
                
                <p>Organization: {}</p>
                <p>Contract Number: {}</p>
                <p>Contract Holder Name: {}</p>
                <p>Class: {}</p>
                <p>Member Name: {}</p>
                <p>ID Number: {}</p>
                
                
                <h3 style="margin-top: 30px;">Information Summary</h3>
                
                <p>Total Benefit Credits: {}</p>
                <p>Current HSA Selection: {}</p>
                <p>Benefit Credits Remaining: {}</p>
            
            </body>
        </html>
    """.format(member.org.org_short_name, member.org.policy_num, member.org.contract_holder, member.org.class_type, name, member.username, member.hsa_annual_credits,
               hsa_optional, new_hsa_remaining)



    if member.opt_out_bool:
        add_to_body = """
            <p>Salary Base: {}</p>
            <p>Salary Adjusted: {}</p>
        """.format(member.salary_base, salary_adjusted)

        body = body + add_to_body



    msg.attach(MIMEText(body, 'html'))


    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    server.login(fromaddr, "E<43BQqK")

    text = msg.as_string()

    server.sendmail(fromaddr, toaddr, text)
    server.quit()

    print("mail sent!!!")



@task(name='sent_hsa_detail_to_admin')
def sent_hsa_detail_to_admin(member_id, hsa_optional, new_hsa_remaining, salary_adjusted):
    member = account_model.UserProfile.objects.get(id=member_id)

    fromaddr = "dmasl_enrolment@volfson.ca"
    toaddr = member.org.admin_email

    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr

    msg['Subject'] = "A member just enroll HSA in dmasl"


    name = None

    if member.last_name:
        name = member.last_name

    if member.first_name:
        name += " " +member.first_name

    if member.middle_name:
        name += " " + member.middle_name


    body = """
        <!html>
            <head>
                <style></style>
            </head>
            
            <body>
                
                <h2>Member enrolment application details is below: </h2>
                
                <h3 style="margin-top: 30px;">Member detail</h3>
                
                <p>Organization: {}</p>
                <p>Contract Number: {}</p>
                <p>Contract Holder Name: {}</p>
                <p>Class: {}</p>
                <p>Member Name: {}</p>
                <p>ID Number: {}</p>
                
                
                <h3 style="margin-top: 30px;">Information Summary</h3>
                
                <p>Total Benefit Credits: {}</p>
                <p>Current HSA Selection: {}</p>
                <p>Benefit Credits Remaining: {}</p>
            
            </body>
        </html>
    """.format(member.org.org_short_name, member.org.policy_num, member.org.contract_holder, member.org.class_type, name, member.username, member.hsa_annual_credits,
               hsa_optional, new_hsa_remaining)



    if member.opt_out_bool:
        add_to_body = """
            <p>Salary Base: {}</p>
            <p>Salary Adjusted: {}</p>
        """.format(member.salary_base, salary_adjusted)

        body = body + add_to_body



    msg.attach(MIMEText(body, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    server.login(fromaddr, "E<43BQqK")

    text = msg.as_string()

    server.sendmail(fromaddr, toaddr, text)
    server.quit()


    print("mail sent!!!")

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The smtplib module defines an SMTP client session object that can be used to send mail
# to any Internet machine with an SMTP or ESMTP listener daemon. For details of SMTP and
# ESMTP operation, consult RFC 821 (Simple Mail Transfer Protocol)
# and RFC 1869 (SMTP Service Extensions).
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from PythonScripts.Imports import Config


def sendMailWithSingleZipFile(to, subject, text, filename):
    msg = MIMEMultipart()
    msg['From'] = Config.get_email_user_name()
    msg['To'] = str(to)
    msg['Subject'] = subject
    text += '\nDatei in .zip umbenennen und einfach auspacken!\n\n'
    msg.attach(MIMEText(text))

    zipMsg = MIMEBase('application', 'zip')
    with open(filename, mode='r') as file:
        zipMsg.set_payload(file.read())
    encoders.encode_base64(zipMsg)
    zipMsg.add_header('Content-Disposition', 'attachment', filename=filename + "x")
    msg.attach(zipMsg)

    do_send_mail(msg)


def sendMailWithTextBody(to, subject, text):
    msg = MIMEMultipart()
    msg['From'] = Config.get_email_user_name()
    msg['To'] = str(to)
    msg['Subject'] = subject
    msg.attach(MIMEText(text))

    do_send_mail(msg)


def sendMailWithBodyFromFile(to, subject, filename):
    msg = MIMEMultipart()
    msg['From'] = Config.get_email_user_name()
    msg['To'] = str(to)
    msg['Subject'] = subject
    with open(filename, mode='r') as file:
        msg.attach(MIMEText(file.read()))

    do_send_mail(msg)


def do_send_mail(mime_message):
    username = Config.get_email_user_name()
    password = Config.get_email_password()
    server = smtplib.SMTP(Config.get_email_server_address())
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail(mime_message['From'], mime_message['To'], mime_message.as_string())
    server.quit()

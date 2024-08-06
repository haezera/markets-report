from nbconvert import HTMLExporter
from nbconvert.preprocessors import ExecutePreprocessor
import smtplib
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText 
import asyncio
import datetime as dt
import nbformat
import os
import datetime
from config import *

today = dt.datetime.today().strftime("%Y-%m-%d")

receivers = ["haeohreum09@hotmail.com"]
subject = f"Daily Markets Report {today}"

html_exporter = HTMLExporter()
html_exporter.exclude_input = True
with open("./report.ipynb") as f:
    nb = nbformat.read(f, as_version=4)
ep = ExecutePreprocessor(timeout=-1)
ep.preprocess(nb)

html_data, _ = html_exporter.from_notebook_node(nb)

try:
    with smtplib.SMTP(smtp_name, smtp_port) as client:
        client.starttls()
        client.login(email, pw)
        for receiver in receivers:
            message = MIMEMultipart("alternative")
            message["From"] = email
            message["To"] = receiver
            message["Subject"] = subject
            attachment = MIMEText(html_data, "html")
            attachment.add_header(
                "Content-Disposition",
                "attachment; filename=report.html"
            )
            message.attach(attachment)

            client.sendmail(email, receiver, message.as_string())
except Exception as e:
    print(f"Exception {e} was thrown while sending.")
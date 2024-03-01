from celery import shared_task
from django.core.mail import send_mail
import os

@shared_task
def send_contact_mail(full_name, email, mobile_number, email_subject, message):
    email_body = f"From: {full_name}\n"
    if email:
        email_body += f"Email: {email}\n"
    if mobile_number:
        email_body += f"Mobile Number: {mobile_number}\n"
    email_body += f"\n{message}"

    send_mail(
        subject=email_subject,
        message=email_body,
        recipient_list=['harijordan95@gmail.com'],
    )


import logging

from django.core.mail import send_mail
from django.http import JsonResponse

from base.backend.service import StateService, NotificationService
from core.backend.status import SheltuzNotify
from sheltuz import settings

notify = SheltuzNotify()

lgr = logging.getLogger(__name__)


def send_user_email(**kwargs):
	"""
	- Here we email the user with password
	- First we get the username, user email and password
	- From there we use the send_mail function to send the email to a specified user
	- Username is the name of the user that is getting registered
	- we get the email that the user enters during registration
	- Email from is the system email that is supposed to be sending passwords to new users
	- Subject is the title of the mail we are sending
	- Recipient_list is the email that is going to receive the passwords
	- We use the send_mail to submit the email
	"""
	try:
		email = kwargs.get('email')
		message = kwargs.get('message')
		subject = kwargs.get('subject')
		email_from = settings.EMAIL_HOST_USER
		recipient_list = [email, ]
		if not subject or not message:
			lgr.exception("Failed to send email")
			return JsonResponse({"code": notify.failed(), "message": "Failed to send email"})
		send_mail(subject, message, email_from, recipient_list)
		NotificationService().create(name=recipient_list, description=message, state=StateService().get(name="Sent"))
		return {"code": notify.success(), "message": "success"}
	except Exception as e:
		lgr.exception("Failed to send email", str(e))
		return JsonResponse({"code": notify.failed(), "message": "Failed to send email"})

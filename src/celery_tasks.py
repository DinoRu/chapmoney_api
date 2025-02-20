from celery import  Celery
from asgiref.sync import async_to_sync

from src.config import Config
from src.mail import create_message, mail

app = Celery('chapmoney')
app.config_from_object("src.config")

@app.task()
def send_mail(recipients: list[str], body: str, subject: str):
	message = create_message(
		recipients=recipients,
		body=body,
		subject=subject
	)
	async_to_sync(mail.send_message)(message)
	print("Email sent")
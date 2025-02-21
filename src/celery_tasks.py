from celery import  Celery
from asgiref.sync import async_to_sync
from src.mail import create_message, mail

app = Celery('chapmoney')
app.config_from_object("src.config")

@app.task()
def send_email(recipients: list[str], subject: str, body: str):
	message = create_message(
		recipients=recipients,
		body=body,
		subject=subject
	)
	async_to_sync(mail.send_message)(message)
	print("Email sent")
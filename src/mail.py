from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from src.config import Config

mail_conf = ConnectionConfig(
    MAIL_USERNAME = Config.MAIL_USERNAME,
    MAIL_PASSWORD = Config.MAIL_PASSWORD,
    MAIL_FROM = Config.MAIL_FROM,
    MAIL_PORT = Config.MAIL_PORT,
    MAIL_SERVER = Config.MAIL_SERVER,
    MAIL_FROM_NAME= Config.MAIL_FROM_NAME,
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

mail = FastMail(
    config=mail_conf
)

def create_message(
        recipients: list[str], subject: str, body: str
):
    messages = MessageSchema(
        recipients=recipients,
        subject=subject, body=body,
        subtype=MessageType.html
    )

    return messages


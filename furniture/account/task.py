from celery import shared_task
from furniture.celery import app
from django.core.mail import EmailMessage
import logging

#logger = logging.getLogger(__name__)
logger = logging.getLogger('django')

#@shared_task
@app.task(name="worker")
def send_verification_email(mail_title, message_data, mail_to):
    try:
        email = EmailMessage(mail_title, message_data, to=[mail_to])
        email.send()
        logger.info(f"이메일이 성공적으로 전송되었습니다: {mail_to}")
    except Exception as e:
        logger.error(f"이메일 전송 실패: {e}")
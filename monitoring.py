import smtplib  
from email.mime.text import MIMEText 
import logging

logger = logging.getLogger(__name__)


SMPT_SERVER =  "smtp.mail.ru"
SMPT_PORT = 587
SMPT_PASSWORD = "dNR3EqyEa08GENgp3ejB"
SMPT_USER = "t.test@rtk-bianalitika.bizml.ru"
ADMIN_EMAIL = "arinapatak71@gmail.com"


def send_alert(subject, message):
    try:
        msg = MIMEText(message) 
        msg['Subject']=subject 
        msg['From'] = SMPT_USER 
        msg['To']=ADMIN_EMAIL
        with smtplib.SMTP(SMPT_SERVER,SMPT_PORT) as server: 
            server.starttls() 
            server.login(SMPT_USER,SMPT_PASSWORD)
            server.send_message(msg)
        logger.info("Уведомление отправлено")
    except Exception as e:
        logger.error(f"Ошибка отправки уведомления {e}")





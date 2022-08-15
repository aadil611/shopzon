from celery import shared_task
import smtplib,ssl

@shared_task(bind=True)
def send_mail(self,sender,receiver,password,message):
  context = ssl.create_default_context()
  with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as server:
        server.login(sender,password)
        server.sendmail(sender,receiver,message)
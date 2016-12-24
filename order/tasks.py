# Create your tasks here
from __future__ import absolute_import, unicode_literals
from waterlily.settings import celery_app, WTS_HELPER


@celery_app.task
def send_sms(mobile, message):
    WTS_HELPER.send_sms(mobile, message)


@celery_app.task
def minus(x, y):
    return x - y
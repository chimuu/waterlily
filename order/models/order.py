from __future__ import unicode_literals

import datetime
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Order(models.Model):
    serial_no = models.IntegerField(default=0)
    customer_name = models.CharField(max_length=100)
    customer_mobile = models.BigIntegerField()
    customer_address = models.CharField(max_length=1000)
    measurements = JSONField()
    bill = JSONField()
    delivery_date = models.DateTimeField()
    image_url = models.URLField(max_length=1000, null=True)
    text = models.TextField(null=True)
    user = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tailor_order'
        unique_together = (('serial_no', 'user'),)

@receiver(post_save, sender=Order, dispatch_uid="updatd_text")
def update_stock(sender, instance, **kwargs):
     text = '{}|{}|{}'.format(instance.serial_no, instance.customer_name, instance.customer_mobile)
     sender.objects.filter(pk=instance.pk).update(text=text)

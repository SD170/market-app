from django.contrib.auth.models import User,Group

from django.db.models.signals import post_save

from django.dispatch import receiver
from .models import *

# @receiver(post_save, sender=User)
def create_customer (sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='customer')
        instance.groups.add(group)
    
        Customer.objects.create(
				user=instance,
				name=instance.username,
			)
post_save.connect(create_customer, sender=User)

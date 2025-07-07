from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from panel.models import Mailing, UserCode



@receiver(post_save, sender=Mailing)
def mailing_post_save(sender, instance: Mailing, created, **kwargs):
    from panel.tasks import send_mailing

    if created:
        transaction.on_commit(lambda: send_mailing.apply_async(args=[instance.id], eta=instance.datetime))
        
        
@receiver(post_save, sender=UserCode)
def mailing_post_save(sender, instance: UserCode, created, **kwargs):
    from panel.tasks import delete_message

    if created:
        transaction.on_commit(lambda: delete_message.apply_async(args=[instance.user_id, instance.qr_message_id], countdown=300 ))

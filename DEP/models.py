from django.db import models


class MyModel(models.Model):
    class Meta:
        permissions = (
            ('can_delete_device_id', 'User can delete Device ID.'),
        )

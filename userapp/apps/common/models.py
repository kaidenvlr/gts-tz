from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    @property
    def ago(self):
        return (timezone.now() - self.created_at).total_seconds()

    def __str__(self):
        return f"{self.created_at}, {self.updated_at}"

    class Meta:
        abstract = True
        ordering = ['-created_at', '-updated_at']


class ActivationBaseModel(models.Model):
    is_active = models.BooleanField(_("Is active"), default=True)

    class Meta:
        abstract = True

    def activate(self):
        self.is_active = True
        self.save(update_fields=("is_active",))

    def deactivate(self):
        self.is_active = False
        self.save(update_fields=("is_active",))

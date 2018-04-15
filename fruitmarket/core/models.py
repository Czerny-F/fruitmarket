from django.db import models
from django.utils.translation import ugettext_lazy as _


class EditableModel(models.Model):
    updated_at = models.DateTimeField(_("datetime updated"), auto_now=True)
    created_at = models.DateTimeField(_("datetime created"), auto_now_add=True)

    class Meta:
        abstract = True

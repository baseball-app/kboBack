from django.db import models
from django.utils.translation import gettext_lazy as _


class CreatedTimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created_at"))

    class Meta:
        abstract = True


class UpdatedTimeStampModel(models.Model):
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated_at"))

    class Meta:
        abstract = True


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created_at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated_at"))

    class Meta:
        abstract = True


class AuditModel(models.Model):
    created_user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, verbose_name=_("created_user"))
    updated_user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, verbose_name=_("updated_user"))

    class Meta:
        abstract = True


class AuditTimeStampModel(AuditModel, TimeStampModel):
    created_user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, verbose_name=_("created_user"))
    updated_user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, verbose_name=_("updated_user"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created_at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated_at"))

    class Meta:
        abstract = True

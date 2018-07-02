from django.db import models


class TimeStampedModel(models.Model):
    """ An abstract base class model that provides self- updating ``created`` and ``modified`` fields. """

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SmallIntegerRangeField(models.SmallIntegerField):
    # TODO: test this
    def __init__(
        self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs
    ):
        self.min_value = min_value
        self.max_value = max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {"min_value": self.min_value, "max_value": self.max_value}
        defaults.update(kwargs)
        return super(SmallIntegerRangeField, self).formfield(**defaults)

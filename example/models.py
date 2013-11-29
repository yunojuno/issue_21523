# coding=utf-8
import datetime
from django.db import models

class ModelWithDateField(models.Model):
    """A model that has a single DateField, for testing mock issues."""
    test_field = models.DateField()

    def save(self):
        """Sets the test_field to datetime.date.today() and saves model."""
        self.test_field = datetime.date.today()
        super(ModelWithDateField, self).save()
        return self

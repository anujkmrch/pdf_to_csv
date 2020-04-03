from django.db import models


class Csv(models.Model):
    """  """
    slug = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.slug


class Journal(models.Model):
    csv = models.ForeignKey(
        Csv, on_delete=models.DO_NOTHING,)
    npa_key = models.CharField(
        max_length=100, default=None, blank=None, null=True)
    npa_val = models.CharField(
        max_length=100, default=None, blank=None, null=True)

    def __str__(self):
        return self.npa_key

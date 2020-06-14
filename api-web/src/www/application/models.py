from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from . import constants

class Chromosome(models.Model):
    code = models.CharField(max_length=50, default='')
    is_good_quality = models.BooleanField(default=False)

class Gene(models.Model):
    code = models.CharField(max_length=50, default='')
    is_good_quality = models.BooleanField(default=False)

class Variation(models.Model):
    code = models.CharField(max_length=50, default='')
    is_good_quality = models.BooleanField(default=False)

class Publication(models.Model):
    code = models.CharField(max_length=50, default='')
    is_good_quality = models.BooleanField(default=False)

class Disease(models.Model):
    code = models.CharField(max_length=50, default='')
    is_good_quality = models.BooleanField(default=False)

class Trait(models.Model):
    code = models.CharField(max_length=50, default='')
    is_good_quality = models.BooleanField(default=False)

class Treatment(models.Model):
    code = models.CharField(max_length=50, default='')
    is_good_quality = models.BooleanField(default=False)

class Exon(models.Model):
    code = models.CharField(max_length=50, default='')
    is_good_quality = models.BooleanField(default=False)

class Drug(models.Model):
    code = models.CharField(max_length=50, default='')
    is_good_quality = models.BooleanField(default=False)

class Accession(models.Model):
    code = models.CharField(max_length=50, default='')
    reference_assembly = models.CharField(max_length=255, default='')
    chromosome = models.CharField(max_length=255, default='')
    length = models.IntegerField(default=0)

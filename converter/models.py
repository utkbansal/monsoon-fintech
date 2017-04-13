# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Year(models.Model):
    value = models.CharField(max_length=4)

    def __unicode__(self):
        return self.value


class Variable(models.Model):
    name = models.CharField(max_length=256)

    def __unicode__(self):
        return self.name


class Data(models.Model):
    amount = models.FloatField()
    year = models.ForeignKey(Year)
    variable = models.ForeignKey(Variable)

    def __unicode__(self):
        return str(self.amount) + ' ' + self.variable.name + ' ' + self.year.value

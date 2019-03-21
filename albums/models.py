# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

class NSDA(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    slug = models.SlugField(max_length=150, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True, verbose_name="Activo")

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        abstract = True


class Album(NSDA):
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    artist = models.ForeignKey('ArtistGroup', blank=True, null=True, related_name='artists')

class ArtistGroupType(NSDA): pass


class ArtistGroup(NSDA):
    otype = models.ForeignKey(ArtistGroupType, null=True, blank=True)


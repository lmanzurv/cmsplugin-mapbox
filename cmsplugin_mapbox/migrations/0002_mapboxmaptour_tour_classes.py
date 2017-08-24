# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmsplugin_mapbox', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mapboxmaptour',
            name='tour_classes',
            field=models.CharField(max_length=250, null=True, verbose_name='CSS classes', blank=True),
        ),
    ]

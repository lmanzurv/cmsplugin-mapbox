# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmsplugin_mapbox', '0004_auto_20160810_0526'),
    ]

    operations = [
        migrations.AddField(
            model_name='mapboxmaplegend',
            name='show_all_text',
            field=models.CharField(max_length=250, null=True, verbose_name='Show All Label', blank=True),
        ),
        migrations.AlterField(
            model_name='mapboxmaplegend',
            name='show_all',
            field=models.BooleanField(default=True, verbose_name='Show All Option'),
        ),
    ]

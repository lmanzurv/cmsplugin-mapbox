# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmsplugin_mapbox', '0003_auto_20160729_0749'),
    ]

    operations = [
        migrations.AddField(
            model_name='mapboxmaplegend',
            name='scroll_more_icon',
            field=models.CharField(max_length=50, null=True, verbose_name='Scroll for more icon', blank=True),
        ),
        migrations.AddField(
            model_name='mapboxmaplegend',
            name='scroll_more_text',
            field=models.CharField(max_length=250, null=True, verbose_name='Scroll for more text', blank=True),
        ),
    ]

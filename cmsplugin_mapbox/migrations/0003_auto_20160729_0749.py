# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('cmsplugin_mapbox', '0002_mapboxmaptour_tour_classes'),
    ]

    operations = [
        migrations.AddField(
            model_name='mapboxmappoint',
            name='icon_url',
            field=models.URLField(default=b'', max_length=250, verbose_name='Icon URL'),
        ),
        migrations.AlterField(
            model_name='mapboxmap',
            name='zoom',
            field=models.FloatField(default=5, null=True, verbose_name='Initial Zoom', blank=True),
        ),
        migrations.AlterField(
            model_name='mapboxmaptour',
            name='name',
            field=models.CharField(max_length=250, verbose_name='Tour Name', validators=[django.core.validators.RegexValidator(b'^([a-zA-Z0-9]+)$', message='The name must be alphanumeric', code=b'invalid_name')]),
        ),
    ]

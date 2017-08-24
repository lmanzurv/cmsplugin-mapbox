# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0013_urlconfrevision'),
    ]

    operations = [
        migrations.CreateModel(
            name='MapBoxMap',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('name', models.CharField(max_length=90, verbose_name='Map Name')),
                ('mapbox_access_token', models.CharField(max_length=90, verbose_name='Mapbox Access Token')),
                ('mapbox_style', models.CharField(max_length=250, verbose_name='Mapbox URL for Style')),
                ('latitude', models.FloatField(verbose_name='Initial Latitude')),
                ('longitude', models.FloatField(verbose_name='Initial Longitude')),
                ('zoom', models.FloatField(default=5, verbose_name='Initial Zoom')),
                ('zoom_scroll', models.BooleanField(default=True, verbose_name='Allow Zoom Scrolling')),
                ('zoom_to_tours', models.BooleanField(default=True, verbose_name='Resize to Fit Markers')),
                ('map_classes', models.CharField(max_length=250, null=True, verbose_name='Map Container CSS classes', blank=True)),
            ],
            options={
                'verbose_name': 'MapBox Map',
                'verbose_name_plural': 'MapBox Maps',
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='MapBoxMapLegend',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=250, verbose_name='Legend Title')),
                ('show_all', models.BooleanField(default=True, verbose_name='Show All Option in Legend')),
                ('legend_classes', models.CharField(max_length=250, null=True, verbose_name='Legend CSS classes', blank=True)),
                ('button_classes', models.CharField(max_length=250, null=True, verbose_name='Show Legend Button CSS classes', blank=True)),
                ('map', models.ForeignKey(related_name='legend_map', to='cmsplugin_mapbox.MapBoxMap')),
            ],
        ),
        migrations.CreateModel(
            name='MapBoxMapPoint',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('name', models.CharField(max_length=250, verbose_name='Point Name')),
                ('latitude', models.FloatField(verbose_name='Latitude')),
                ('longitude', models.FloatField(verbose_name='Longitude')),
                ('icon_name', models.CharField(max_length=250, verbose_name='Icon Name')),
            ],
            options={
                'verbose_name': 'MapBox Map Point',
                'verbose_name_plural': 'MapBox Map Points',
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='MapBoxMapTour',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('name', models.CharField(max_length=250, verbose_name='Tour Name')),
                ('legend_text', models.CharField(max_length=250, verbose_name='Legend Text')),
                ('color', models.CharField(max_length=7, verbose_name='Color', validators=[django.core.validators.RegexValidator(b'^(#)?([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', message='Color must be hexadecimal', code=b'invalid_color')])),
            ],
            options={
                'verbose_name': 'MapBox Map Tour',
                'verbose_name_plural': 'MapBox Map Tours',
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='MapBoxTourRoute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('angle', models.IntegerField(default=0, verbose_name='Angle')),
                ('line_width', models.IntegerField(default=2, verbose_name='Line Width')),
                ('finish_point', models.ForeignKey(related_name='route_finish_point', verbose_name='Finish Point', to='cmsplugin_mapbox.MapBoxMapPoint')),
                ('initial_point', models.ForeignKey(related_name='route_initial_point', verbose_name='Initial Point', to='cmsplugin_mapbox.MapBoxMapPoint')),
                ('tour', models.ForeignKey(related_name='route_tour', to='cmsplugin_mapbox.MapBoxMapTour')),
            ],
        ),
    ]

# -*- coding: utf-8 -*-
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import MapBoxMap, MapBoxMapLegend, MapBoxMapPoint, MapBoxMapTour, MapBoxTourRoute

class MapBoxMapLegendInline(admin.StackedInline):
    model = MapBoxMapLegend
    extra = 1
    min_num = 1
    max_num = 1
    can_delete = False
    verbose_name = _('Legend')
    verbose_name_plural = _('Legends')

class MapBoxMapPlugin(CMSPluginBase):
    model = MapBoxMap
    inlines = [MapBoxMapLegendInline]
    name = _('MapBox Map')
    module = _('MapBox')
    render_template = 'mapbox_map.html'
    allow_children = True
    child_classes = ['MapBoxMapPointPlugin', 'MapBoxMapTourPlugin']

    fieldsets = (
        (None, {
            'fields': [
                'name',
                'map_classes'
            ]
        }),
        (_('MapBox'), {
            'fields': [
                'mapbox_access_token',
                'mapbox_style',
                'latitude',
                'longitude',
                'zoom',
                'zoom_scroll',
                'zoom_to_tours'
            ]
        }),
    )

    def render(self, context, instance, placeholder):
        context = super(MapBoxMapPlugin, self).render(context, instance, placeholder)
        return context

plugin_pool.register_plugin(MapBoxMapPlugin)

class MapBoxMapPointPlugin(CMSPluginBase):
    model = MapBoxMapPoint
    name = _('MapBox Map Point')
    module = _('MapBox')
    render_template = 'mapbox_map_point.html'
    require_parent = True
    parent_classes = ['MapBoxMapPlugin']

    def render(self, context, instance, placeholder):
        context = super(MapBoxMapPointPlugin, self).render(context, instance, placeholder)
        return context

plugin_pool.register_plugin(MapBoxMapPointPlugin)

class MapBoxMapTourRoutesInline(admin.TabularInline):
    model = MapBoxTourRoute
    extra = 0

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        try:
            tour = MapBoxMapTour.objects.get(cmsplugin_ptr_id=request.resolver_match.args[0])
            language = tour.language
        except:
            referer = request.META['HTTP_REFERER']
            language = referer.split('/')[3]

        if db_field.name == 'initial_point' or db_field.name == 'finish_point':
            kwargs['queryset'] = MapBoxMapPoint.objects.filter(placeholder__page__publisher_is_draft=True, language=language)
        return super(MapBoxMapTourRoutesInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

class MapBoxMapTourPlugin(CMSPluginBase):
    model = MapBoxMapTour
    inlines = [MapBoxMapTourRoutesInline]
    name = _('MapBox Map Tour')
    module = _('MapBox')
    render_template = 'mapbox_map_tour.html'
    require_parent = True
    parent_classes = ['MapBoxMapPlugin']
    allow_children = True

    def render(self, context, instance, placeholder):
        context = super(MapBoxMapTourPlugin, self).render(context, instance, placeholder)
        return context

plugin_pool.register_plugin(MapBoxMapTourPlugin)

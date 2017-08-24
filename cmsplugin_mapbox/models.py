# -*- coding: utf-8 -*-
from django.db import models
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

class MapBoxMap(CMSPlugin):
    name = models.CharField(max_length=90, verbose_name=_('Map Name'))
    mapbox_access_token = models.CharField(max_length=90, verbose_name=_('Mapbox Access Token'))
    mapbox_style = models.CharField(max_length=250, verbose_name=_('Mapbox URL for Style'))
    latitude = models.FloatField(verbose_name=_('Initial Latitude'))
    longitude = models.FloatField(verbose_name=_('Initial Longitude'))
    zoom = models.FloatField(default=5, verbose_name=_('Initial Zoom'), null=True, blank=True)
    zoom_scroll = models.BooleanField(default=True, verbose_name=_('Allow Zoom Scrolling'))
    zoom_to_tours = models.BooleanField(default=True, verbose_name=_('Resize to Fit Markers'))
    map_classes = models.CharField(max_length=250, verbose_name=_('Map Container CSS classes'), null=True, blank=True)

    def legend(self):
        legend = None
        try:
            legend = MapBoxMapLegend.objects.get(map_id=self.id)
        except:
            pass
        return legend

    def copy_relations(self, oldinstance):
        legend = oldinstance.legend()
        legend.pk = None
        legend.map = self
        legend.save()

    class Meta:
        verbose_name = _('MapBox Map')
        verbose_name_plural = _('MapBox Maps')

    def __unicode__(self):
        return self.name

class MapBoxMapLegend(models.Model):
    map = models.ForeignKey(MapBoxMap, related_name='legend_map')
    title = models.CharField(max_length=250, verbose_name=_('Legend Title'))
    show_all = models.BooleanField(default=True, verbose_name=_('Show All Option'))
    show_all_text = models.CharField(max_length=250, verbose_name=_('Show All Label'), null=True, blank=True)
    legend_classes = models.CharField(max_length=250, verbose_name=_('Legend CSS classes'), null=True, blank=True)
    button_classes = models.CharField(max_length=250, verbose_name=_('Show Legend Button CSS classes'), null=True, blank=True)
    scroll_more_text = models.CharField(max_length=250, verbose_name=_('Scroll for more text'), null=True, blank=True)
    scroll_more_icon = models.CharField(max_length=50, verbose_name=_('Scroll for more icon'), null=True, blank=True)

    def _unicode__(self):
        return ''

class MapBoxMapPoint(CMSPlugin):
    name = models.CharField(max_length=250, verbose_name=_('Point Name'))
    latitude = models.FloatField(verbose_name=_('Latitude'))
    longitude = models.FloatField(verbose_name=_('Longitude'))
    icon_name = models.CharField(max_length=250, verbose_name=_('Icon Name'))
    icon_url = models.URLField(max_length=250, verbose_name=_('Icon URL'), default='')

    class Meta:
        verbose_name = _('MapBox Map Point')
        verbose_name_plural = _('MapBox Map Points')

    def __unicode__(self):
        return '%s' % (self.name)

class MapBoxMapTour(CMSPlugin):
    name = models.CharField(max_length=250, verbose_name=_('Tour Name'), validators=[RegexValidator(r'^([a-zA-Z0-9]+)$',
        message=_('The name must be alphanumeric'), code='invalid_name')])
    legend_text = models.CharField(max_length=250, verbose_name=_('Legend Text'))
    color = models.CharField(max_length=7, verbose_name=_('Color'), validators=[RegexValidator(r'^(#)?([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
        message=_('Color must be hexadecimal'), code='invalid_color')])
    tour_classes = models.CharField(max_length=250, verbose_name=_('CSS classes'), null=True, blank=True)

    @property
    def routes(self):
        return MapBoxTourRoute.objects.filter(tour_id=self.id)

    def copy_relations(self, oldinstance):
        for tour_route in oldinstance.route_tour.all():
            tour_route.pk = None
            tour_route.tour = self
            tour_route.save()

    def clean(self):
        manager = self.__class__.objects
        # FIXME This is needs to be validated in new tours too
        if self.placeholder:
            self.is_draft = self.placeholder.page.publisher_is_draft
            if manager.filter(name=self.name, language=self.language, placeholder__page__publisher_is_draft=self.is_draft).exclude(id=self.id).exists():
                raise ValidationError('The name property must be unique')

    class Meta:
        verbose_name = _('MapBox Map Tour')
        verbose_name_plural = _('MapBox Map Tours')

    def __unicode__(self):
        return self.legend_text

class MapBoxTourRoute(models.Model):
    tour = models.ForeignKey(MapBoxMapTour, related_name='route_tour')
    initial_point = models.ForeignKey(MapBoxMapPoint, verbose_name=_('Initial Point'), related_name='route_initial_point')
    finish_point = models.ForeignKey(MapBoxMapPoint, verbose_name=_('Finish Point'), related_name='route_finish_point')
    angle = models.IntegerField(default=0, verbose_name=_('Angle'))
    line_width = models.IntegerField(default=2, verbose_name=_('Line Width'))

    def __unicode__(self):
        return ''

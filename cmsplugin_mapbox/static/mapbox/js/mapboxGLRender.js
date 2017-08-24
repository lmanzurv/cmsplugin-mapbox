var mapboxGLMapGenerator = function() {
    var map;
    var language;
    var points;
    var map_name;
    var map_resize;
    var map_scrollZoom;
    var layer_visibility;

    var renderMap = function(configurations, points, tours, loadMap) {
        mapboxgl.accessToken = configurations.accessToken;

        map_options = {
            container: 'mapbox-map-'+map_name,
            style: configurations.mapStyle,
            center: [configurations.initLongitude, configurations.initLatitude],
            scrollZoom: !map_scrollZoom
        };

        if(configurations.hasOwnProperty('initZoom')) {
            map_options['zoom'] = configurations.initZoom - 1;
        }

        map = new mapboxgl.Map(map_options);

        if(map_scrollZoom) {
            map.scrollZoom.disable();
        }

        map.addControl(new mapboxgl.NavigationControl());

        map.on('load', function () {

            $.each(tours, function(name, tour) {
                var source_name;
                var color;
                var width;

                if(!$.isEmptyObject(tour)) {
                    if(tour.type == 'FeatureCollection') {
                        source_name = tour.features[0].properties.name;
                        color = tour.features[0].properties.color;
                        width = tour.features[0].properties.width;
                    } else {
                        source_name = tour.properties.name;
                        color = tour.properties.color;
                        width = tour.properties.width;
                    }

                    map.addSource(source_name, {
                        'type': 'geojson',
                        'data': tour
                    });

                    map.addLayer({
                        'id': source_name,
                        'type': 'line',
                        'source': source_name,
                        'layout': {
                            'line-join': 'round',
                            'line-cap': 'round',
                            'visibility': 'visible'
                        },
                        'paint': {
                            'line-color': color,
                            'line-width': width
                        }
                    });
                }
            });

            $.each(points, function(name, point) {
                map.addSource(point.properties.name, {
                    'type': 'geojson',
                    'data': point
                });

                map.addLayer({
                    'id': point.properties.name,
                    'type': 'symbol',
                    'source': point.properties.name,
                    'layout': {
                        'icon-image': point.properties['marker-symbol'],
                        'icon-allow-overlap': true,
                        'visibility': 'visible'
                    }
                });
            });

            if(!configurations.hasOwnProperty('initZoom')) {
                var oldMapResize = map_resize;
                map_resize = true;
                processTourSelection(map_name + '-show-all');
                map_resize = oldMapResize;
            }

            map.setLayoutProperty('country_label_big', 'text-field', '{name_' + language + '}');
            map.setLayoutProperty('city_label_big', 'text-field', '{name_' + language + '}');

            loadMap();
        });
    };

    var processTourSelection = function(selected_tour_id) {

        var min_lat = Number.POSITIVE_INFINITY;
        var max_lat = Number.NEGATIVE_INFINITY;

        var min_long = Number.POSITIVE_INFINITY;
        var max_long = Number.NEGATIVE_INFINITY;

        if(selected_tour_id == map_name+'-show-all') {
            $('.mapboxgl-ctrl-attrib .mapboxgl-ctrl').hide();
            $.each(layer_visibility, function(layerID, visibility) {
                map.setLayoutProperty(layerID, 'visibility','visible');
                if(layerID in points) {
                    if(points[layerID].geometry.coordinates[0]<min_lat) {
                        min_lat = points[layerID].geometry.coordinates[0];
                    } else if (points[layerID].geometry.coordinates[0]>max_lat) {
                        max_lat = points[layerID].geometry.coordinates[0];
                    }

                    if(points[layerID].geometry.coordinates[1]<min_long) {
                        min_long = points[layerID].geometry.coordinates[1];
                    } else if (points[layerID].geometry.coordinates[1]>max_long) {
                        max_long = points[layerID].geometry.coordinates[1];
                    }
                }

            });
        } else {
            $('.mapboxgl-ctrl-attrib .mapboxgl-ctrl').show();
            $.each(layer_visibility, function(layerID, visibility) {
                if(visibility[selected_tour_id] == true) {
                    map.setLayoutProperty(layerID, 'visibility','visible');
                    if(layerID in points) {

                        if(points[layerID].geometry.coordinates[0]<min_lat) {
                            min_lat = points[layerID].geometry.coordinates[0];
                        }

                        if (points[layerID].geometry.coordinates[0]>max_lat) {
                            max_lat = points[layerID].geometry.coordinates[0];
                        }

                        if(points[layerID].geometry.coordinates[1]<min_long) {
                            min_long = points[layerID].geometry.coordinates[1];
                        }

                        if (points[layerID].geometry.coordinates[1]>max_long) {
                            max_long = points[layerID].geometry.coordinates[1];
                        }
                    }
                } else {
                    map.setLayoutProperty(layerID, 'visibility','none');
                }
            });
        }

        if (map_resize) {
            map.fitBounds([ [min_lat-1.5, min_long-1.5], [ max_lat+1.5, max_long+1.5] ]);
        }
    };

    var updateMap = function() {
        var width = $(window).width();
        if (width < 768) {
            map.dragPan.disable();
        } else {
            map.dragPan.enable();
        }
    }

    var getMap = function() {
        return map;
    }

    return {
        render: function(lang, map_configurations, map_points, map_tours, visibility, loadMap) {
            language = lang;
            layer_visibility = visibility;
            points = map_points;
            map_name = map_configurations.mapId;
            map_resize = map_configurations.legendResize;
            map_scrollZoom = map_configurations.scrollZoom;
            renderMap(map_configurations, map_points, map_tours, loadMap);
            updateMap();
        },
        selectTour: function(tour_id) {
            processTourSelection(tour_id);
        },
        updateMap: function() {
            updateMap();
        },
        getMap: function() {
            return getMap();
        }
    };
};

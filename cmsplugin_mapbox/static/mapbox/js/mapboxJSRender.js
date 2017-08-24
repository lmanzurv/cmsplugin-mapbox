var mapboxJSMapGenerator = function() {
    var map;
    var layers;
    var map_name;
    var map_resize;
    var map_scrollZoom;
    var layer_visibility;

    var renderMap = function(configurations, points, tours, loadMap) {
        L.mapbox.accessToken = configurations.accessToken;
        map = L.mapbox.map('mapbox-map-'+map_name);

        var initZoom = 1;
        if(configurations.hasOwnProperty('initZoom')) {
            initZoom = configurations.initZoom;
        }
        map.on('load', loadMap).setView([configurations.initLatitude, configurations.initLongitude], initZoom);

        L.mapbox.styleLayer(configurations.mapStyle).addTo(map);
        var map_elements = [];

        $.each(points, function(pt_name, pt_content) {
            var pt_visibility = layer_visibility[pt_name];
            $.each(pt_visibility, function(prt_name, prt_value) {
                pt_content['properties'][prt_name] = prt_value;
            });
            map_elements.push(pt_content);
        });

        $.each(tours, function(tr_name, tr_content) {
            var tr_visibility = layer_visibility[tr_name];
            $.each(tr_visibility, function(prt_name, prt_value) {
                if(tr_content.type == 'Feature') {
                    tr_content['properties'][prt_name] = prt_value;
                } else {
                    if(tr_content.type == 'FeatureCollection') {
                        for(var i=0; i<tr_content.features.length; i++) {
                            tr_content.features[i]['properties'][prt_name] = prt_value;
                        }
                    }
                }
            });
            map_elements.push(tr_content);
        });

        layers = L.mapbox.featureLayer().addTo(map);

        layers.on('layeradd', function(e) {
            var marker = e.layer,
            feature = marker.feature;
            if(feature.properties.icon != null) {
                marker.setIcon(L.icon(feature.properties.icon));
            }
        });

        layers.setGeoJSON(map_elements);

        if(map_scrollZoom) {
            map.touchZoom.disable();
            map.doubleClickZoom.disable();
            map.scrollWheelZoom.disable();
        }

        $('.leaflet-control-attribution').hide();
        processTourSelection(map_name+'-show-all');
    };

    var processTourSelection = function(selected_id) {
        layers.setFilter(function(f) {
            return (selected_id === map_name+'-show-all') ? true : f.properties[selected_id] === true;
        });

        if(map_resize) {
            map.fitBounds(layers.getBounds());
        }
    };

    var updateMap = function() {
        var width = $(window).width();
        if (width < 768) {
            map.dragging.disable();
            if(map.tap) {
                map.tap.disable();
            }
        } else {
            map.dragging.enable();
            if(map.tap) {
                map.tap.enable();
            }
        }
    }

    var getMap = function() {
        return map;
    }

    return {
        render: function(lang, map_configurations, map_points, map_tours, visibility, loadMap) {
            layer_visibility = visibility;
            map_name = map_configurations.mapId;
            map_resize = map_configurations.legendResize;
            map_scrollZoom = map_configurations.scrollZoom;
            renderMap(map_configurations, map_points, map_tours, loadMap);
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

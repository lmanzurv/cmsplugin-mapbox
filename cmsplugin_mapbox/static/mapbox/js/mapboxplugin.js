var MapBoxPlugin = function(language, config, points_config, tours_config, selectedTour) {
    var tours_ids;
    var layer_visbility;
    var map_generator;
    var points;
    var tours;
    var mapboxglSupported;

    var init = function() {
        var ua = window.navigator.userAgent;
        if(ua.indexOf('MSIE') > 0 || ua.indexOf('Trident') > 0) {
            mapboxglSupported = false;
        } else {
            mapboxglSupported = mapboxgl.supported();
        }

        if (mapboxglSupported) {
            map_generator = mapboxGLMapGenerator();
        } else {
            map_generator = mapboxJSMapGenerator();
        }

        layer_visbility = {};
        points = {};
        tours = {};
        tours_ids = [];
        $.each(tours_config, function(tour_name, tour_properties) {
            tours_ids.push(tour_properties.tour_id);
        });

        $('.mapbox-tour-info').hide();
    };

    var showSelectedTour = function (event) {
        var element = event.data.element;
        var selected_tour_id = element.data('tour');

        $('.mapbox-tour-info').hide();
        $('.mapbox-legend-tour').removeClass('selected');
        $('.mapbox-legend-tour').addClass('empty');
        element.removeClass('empty').addClass('selected');
        if(!element.hasClass('show-all')) {
            $('#mapbox-tour-'+selected_tour_id+'-info').show();
        } else {
            $('.mapbox-legend-tour').removeClass('empty');
        }

        map_generator.selectTour(selected_tour_id);

        if(element.hasClass('show-all')) {
            $('.mapbox-arrow-more').css('display', 'none');
            $('.mapbox ~ *:not(script)').css('display', 'none');
        } else {
            $('.mapbox-arrow-more').css('display', 'block');
            $('.mapbox ~ *:not(script)').css('display', 'block');
        }
    };

    var createPointMarkers = function() {
        $.each(points_config, function(pt_name, pt_content) {
            var point = {
                'type': 'Feature',
                'properties': {
                    'name': pt_name,
                    'title': pt_name
                },
                'geometry': {
                    'type': 'Point',
                    'coordinates': [pt_content.longitude, pt_content.latitude]
                }
            };
            if (mapboxglSupported) {
                if (pt_content.icon != null) {
                    point.properties['marker-symbol'] = pt_content.icon;
                } else {
                    point.properties['marker-symbol'] = 'marker_icon';
                }
            } else {
                if (pt_content.icon != null) {
                    point.properties['icon'] = {
                        'iconUrl': pt_content.icon_url,
                        'iconSize': [40,40], // size of the icon
                        'iconAnchor': [25,25], // point of the icon which will correspond to marker's location
                        'className': pt_content.icon
                    }
                }
            }
            points[pt_name] = point;
        });
    };

    var createLines = function() {
        $.each(tours_config, function(tour_name, tour_properties) {
            tour_lines = [];

            if(!(tour_name in layer_visbility)) {
                layer_visbility[tour_name] = {};
            }
            layer_visbility[tour_name][tour_properties.tour_id] = true;

            for(var rt=0; rt<tour_properties.routes.length; rt++) {
                mid_point = generate_three_points_between_two_points(points[tour_properties['routes'][rt]['initPoint']],points[tour_properties['routes'][rt]['finishPoint']],tour_properties['routes'][rt]['angle']);
                var line = {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'LineString',
                        'coordinates': mid_point
                    },
                    'properties': {}
                };

                if(!(tour_properties['routes'][rt]['initPoint'] in layer_visbility)) {
                    layer_visbility[tour_properties['routes'][rt]['initPoint']] = {};
                }

                if(!(tour_properties['routes'][rt]['finishPoint'] in layer_visbility)) {
                    layer_visbility[tour_properties['routes'][rt]['finishPoint']] = {};
                }

                layer_visbility[tour_properties['routes'][rt]['initPoint']][tour_properties.tour_id] = true;
                layer_visbility[tour_properties['routes'][rt]['finishPoint']][tour_properties.tour_id] = true;

                if(typeof turf !== 'undefined') {
                    var line_bezier = turf.bezier(line, 10000, 1.5);
                    var color = tour_properties.color;
                    var width = tour_properties['routes'][rt].line_width

                    line_bezier.properties = { 'name': tour_name };
                    if (mapboxglSupported) {
                        line_bezier.properties['color'] = color;
                        line_bezier.properties['width'] = width;
                    } else {
                        line_bezier.properties['stroke'] = color;
                        line_bezier.properties['stroke-width'] = width;
                    }

                    tour_lines.push(line_bezier);
                }
            }

            if(tour_lines.length === 0) {
                tours[tour_name] = {};
            }
            else if(tour_lines.length === 1) {
                tours[tour_name] = tour_lines[0];
            } else {
                tours[tour_name] = {
                    'type': 'FeatureCollection',
                    'features': tour_lines
                }
            }
        });
    };

    var generate_three_points_between_two_points = function (start, end, angle) {
        //Calculate the midpoint between points
        var startCoords = start.geometry.coordinates;
        var endCoords = end.geometry.coordinates;

        var midCoords;
        if(typeof turf !== 'undefined'){
            var midpoint = turf.midpoint(start, end);
            midCoords = midpoint.geometry.coordinates
        } else {
            if(endCoords[0] > startCoords[0]) {
                midCoords = [endCoords[0] - startCoords[0], endCoords[1] - startCoords[1]];
            } else {
                midCoords = [startCoords[0] - endCoords[0], startCoords[1] - endCoords[1]];
            }
        }

        var x1 = midCoords[0], y1 = midCoords[1], x2 = startCoords[0], y2 = startCoords[1];

        m = (y2 - y1) / (x2 -  x1);
        angle_rad = Math.tan(angle * Math.PI / 180);

        new_y = (angle_rad * (x2 - x1)) + y1;
        new_x = x1 - (m * ( new_y - y1));

        return [startCoords, [new_x, new_y], endCoords];
    };

    var processVisibility = function() {
        for (var key in layer_visbility) {
            if (layer_visbility.hasOwnProperty(key)) {
                for(var i=0; i<tours_ids.length; i++) {
                    if(!(tours_ids[i] in layer_visbility[key])) {
                        layer_visbility[key][tours_ids[i]] = false;
                    }
                }
            }
        }
    };

    var loadMap = function() {
        $('.mapbox-legend-tour').click(function() {
            showSelectedTour({'data': {'element': $(this)}});
        });

        if(selectedTour !== null) {
            showSelectedTour({'data': {'element': $('.mapbox-legend-tour[data-tour-name="' + selectedTour + '"]')}});
        }
    };

    init();

    return {
        generateMap: function() {
            createPointMarkers();
            createLines();
            processVisibility();
            map_generator.render(language, config, points, tours, layer_visbility, loadMap);
        },
        updateMap: function() {
            map_generator.updateMap();
        },
        getMap: function() {
            return map_generator.getMap();
        }
    };
};

/**
 * map.js — Leaflet + CARTO Voyager farm map
 */

var farmMap = null;
var farmMarkers = null;
var radiusCircle = null;
var userMarker = null;

function initMap() {
    farmMap = L.map('map').setView([52.3, -113.5], 6);

    L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a> &copy; <a href="https://carto.com/">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 19,
    }).addTo(farmMap);

    farmMarkers = L.layerGroup().addTo(farmMap);

    // Let user click map to set their location
    farmMap.on('click', function(e) {
        setUserLocation(e.latlng.lat, e.latlng.lng);
    });

    loadFarms();
}

function setUserLocation(lat, lng) {
    document.getElementById('user-lat').value = lat.toFixed(6);
    document.getElementById('user-lng').value = lng.toFixed(6);

    // User pin
    if (userMarker) farmMap.removeLayer(userMarker);
    userMarker = L.circleMarker([lat, lng], {
        radius: 7,
        fillColor: '#E8B931',
        fillOpacity: 1,
        color: '#5C4033',
        weight: 2,
    }).addTo(farmMap).bindTooltip('You are here', {direction: 'top', offset: [0, -10]});

    updateRadiusCircle();

    // Re-fetch results with location
    var form = document.querySelector('.search-bar');
    if (form && typeof htmx !== 'undefined') {
        htmx.trigger(form, 'submit');
    }
}

function updateRadiusCircle() {
    if (!farmMap) return;

    var lat = parseFloat(document.getElementById('user-lat').value);
    var lng = parseFloat(document.getElementById('user-lng').value);
    var radiusKm = parseInt(document.querySelector('[name="radius"]').value) || 50;

    if (isNaN(lat) || isNaN(lng)) return;

    if (radiusCircle) farmMap.removeLayer(radiusCircle);

    radiusCircle = L.circle([lat, lng], {
        radius: radiusKm * 1000,
        color: '#A3B899',
        weight: 2,
        fillColor: '#D4E2C8',
        fillOpacity: 0.12,
        dashArray: '6 4',
    }).addTo(farmMap);

    // Fit map to show the circle
    farmMap.fitBounds(radiusCircle.getBounds(), { padding: [20, 20] });
}

function requestGeolocation() {
    if (!navigator.geolocation) return;
    navigator.geolocation.getCurrentPosition(
        function(pos) {
            setUserLocation(pos.coords.latitude, pos.coords.longitude);
        },
        function() {
            // Denied — user can click the map instead
        },
        { timeout: 8000, maximumAge: 300000 }
    );
}

function loadFarms() {
    if (!farmMap) return;

    var params = new URLSearchParams(window.location.search);
    var url = '/api/farms/map-data/?' + params.toString();

    fetch(url)
        .then(function(r) { return r.json(); })
        .then(function(geojson) {
            farmMarkers.clearLayers();

            var bounds = [];

            if (radiusCircle) {
                bounds.push(radiusCircle.getBounds());
            }

            if (geojson.features && geojson.features.length > 0) {
                geojson.features.forEach(function(feature) {
                    var coords = feature.geometry.coordinates;
                    var props = feature.properties;
                    var lat = coords[1];
                    var lng = coords[0];

                    // Different pin style for markets vs farms
                    var pinOpts = props.type === 'market'
                        ? { radius: 12, fillColor: '#D4A853', fillOpacity: 0.9, color: '#5C4033', weight: 2.5 }
                        : { radius: 10, fillColor: '#4A6741', fillOpacity: 0.9, color: '#FDFAF3', weight: 2.5 };

                    var marker = L.circleMarker([lat, lng], pinOpts);

                    var cats = '';
                    if (props.categories) {
                        var catArr = typeof props.categories === 'string'
                            ? JSON.parse(props.categories) : props.categories;
                        cats = catArr.map(function(c) {
                            return '<span style="display:inline-block;background:#D4E2C8;color:#4A6741;font-size:0.7rem;padding:2px 8px;border-radius:999px;margin:1px 2px;">' + c + '</span>';
                        }).join(' ');
                    }

                    var photoHtml = props.photo && props.photo !== 'null'
                        ? '<img src="' + props.photo + '" style="width:100%;height:100px;object-fit:cover;border-radius:8px 8px 0 0;">'
                        : '<div style="height:50px;background:linear-gradient(135deg,#B5C99A,#87A96B);border-radius:8px 8px 0 0;"></div>';

                    var dateHtml = props.next_date
                        ? '<div style="font-size:0.75rem;color:#D4A853;font-weight:600;margin-top:2px;">Next: ' + props.next_date + '</div>'
                        : '';

                    var linkUrl = props.type === 'market'
                        ? '/markets/' + props.slug + '/'
                        : '/farms/' + props.slug + '/';

                    var html = '<div style="min-width:180px;font-family:DM Sans,system-ui,sans-serif;">'
                        + photoHtml
                        + '<div style="padding:8px;">'
                        + '<strong style="font-family:DM Serif Display,Georgia,serif;color:#5C4033;font-size:1rem;">' + props.name + '</strong>'
                        + '<div style="font-size:0.8rem;color:#6B6B6B;margin-top:2px;">' + (props.address || '') + '</div>'
                        + dateHtml
                        + (cats ? '<div style="margin-top:4px;">' + cats + '</div>' : '')
                        + '<a href="' + linkUrl + '" style="display:inline-block;margin-top:6px;font-size:0.8rem;color:#4A6741;font-weight:500;text-decoration:none;">View details &rarr;</a>'
                        + '</div></div>';

                    marker.bindPopup(html, { maxWidth: 240 });
                    farmMarkers.addLayer(marker);
                    bounds.push([lat, lng]);
                });
            }

            // Only fit bounds if no radius circle (circle already sets bounds)
            if (!radiusCircle && bounds.length > 0) {
                farmMap.fitBounds(bounds, { padding: [40, 40], maxZoom: 12 });
            }
        });
}

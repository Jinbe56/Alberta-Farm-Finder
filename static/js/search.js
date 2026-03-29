/**
 * search.js — Geolocation detection + radius slider output
 * Everything else is handled by HTMX attributes in the templates.
 */

(function () {
    'use strict';

    const latInput = document.getElementById('user-lat');
    const lngInput = document.getElementById('user-lng');

    // Try browser geolocation on page load
    if (navigator.geolocation && latInput && lngInput) {
        navigator.geolocation.getCurrentPosition(
            function (pos) {
                latInput.value = pos.coords.latitude.toFixed(6);
                lngInput.value = pos.coords.longitude.toFixed(6);

                // Re-trigger search with location
                const form = document.querySelector('.search-bar');
                if (form) {
                    htmx.trigger(form, 'submit');
                }
            },
            function () {
                // Geolocation denied or unavailable — search works without distance
                console.log('Geolocation unavailable — showing all farms');
            },
            { timeout: 8000, maximumAge: 300000 }
        );
    }

    // Radius slider label update (also handled by oninput in HTML, but belt-and-suspenders)
    const slider = document.querySelector('.radius-slider');
    const output = document.getElementById('radius-val');
    if (slider && output) {
        slider.addEventListener('input', function () {
            output.textContent = this.value;
        });
    }
})();

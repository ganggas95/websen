// var geoJson = {
//     "type": "FeatureCollection",
//     "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
//     "features": [
//         {
//             "type": "Feature", "properties": { "AREA": 0.003, "PERIMETER": 0.389, "KODE": "029", "NAMA_DAS": "DAS Embarembar" },
//             "geometry": {
//                 "type": "Polygon",
//                 "coordinates": [[[117.26895,-8.403846],[117.237133, -8.516433], [116.399136, -8.213847],[116.353758,-8.386289]]]
//             }
//         },
//     ]
// }


window.onload = function () {
    var map = L.map('maps').setView([-8.6353342, 117.425995], 8);
    // L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
    //     maxZoom: 18,
    //     attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
    //     '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
    //     'Imagery © <a href="http://mapbox.com">Mapbox</a>',
    //     id: 'mapbox.light'
    // }).addTo(map);

    // var geojson = L.geoJson(geoJson).addTo(map);
    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
        maxZoom: 18,
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
        '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
        'Imagery © <a href="http://mapbox.com">Mapbox</a>',
        id: 'mapbox.light'
    }).addTo(map);

    function onEachFeature(feature, layer) {
        var popupContent = "<p>Nama Das : "+feature.properties.DAS_NAME +"</p>"+
            "<p>Kode : "+feature.properties.KODE + "</p>";

        layer.bindPopup(popupContent);
    }

    $.ajax({
        type: "GET",
        url: "/polygons",
        success: function (res) {
            L.geoJSON(res, {
                style: function (feature) {
                    return feature.properties && feature.properties.style;
                },

                onEachFeature: onEachFeature,

                pointToLayer: function (feature, latlng) {
                    return L.circle(latlng, {
                        radius: 200,
                        fillColor: "#ff7800",
                        color: "#000",
                        opacity: 1,
                        fillOpacity: 0.8
                    });
                }
            }).addTo(map);
        }
    });

};
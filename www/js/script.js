var map;
var geojson;
var info;

function getColor(d) {
    return d > 800 ? '#D7301F' :
           d > 300  ? '#FC8D59' :
           d > 80   ? '#FDCC8A' :
           d > 10   ? '#FEF0D9' :
                      '#FFFFFF';
}

function colorstyle(feature) {
    return {
        fillColor: getColor(feature.properties.cases_per_100k),
        weight: 1,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.9
    };
}

function highlightFeature(e) {
    var layer = e.target;

    layer.setStyle({
        weight: 5,
        color: '#666',
        dashArray: '',
        fillOpacity: 0.7
    });

    if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
        layer.bringToFront();
    }
    info.update(layer.feature.properties);
}

function resetHighlight(e) {
    geojson.resetStyle(e.target);
    info.update();
}

function zoomToFeature(e) {
    map.fitBounds(e.target.getBounds());
}

function onEachFeature(feature, layer) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight,
        click: zoomToFeature
    });
}

window.onload = function() {
	map = L.map('mapid').setView([51.317, 12.293], 5);
	
	// Open the base map layer
	L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    	attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
	}).addTo(map);

	// Overlay it with the output geoJSON layer
	geojson = L.geoJSON(testsJSON, {
		style: colorstyle,
		onEachFeature: onEachFeature
	}).addTo(map);

	// The info layer
	info = L.control();
	info.onAdd = function (map) {
    	this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
    	this.update();
    	return this._div;
	};

	// method that we will use to update the control based on feature properties passed
	info.update = function (props) {
	    this._div.innerHTML = (props ? '<h4>' + props. GEN + '</h4>' +  
	        '<b>Cases per 100k</b> : ' + props.cases_per_100k.toFixed(2) + '<br/>' +
	        '<b>Effectiveness</b> : ' + (props.death_rate/20.0).toFixed(2) + '<br/>'  
	        : 'Hover over a county');
	};

	info.addTo(map);
}
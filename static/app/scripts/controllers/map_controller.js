'use strict';

(function(){
  goog.provide('map_controller');

  var module = angular.module('map_controller', ['leaflet-directive']);

  module.controller('MapController', function($scope, $http,
   leafletData, UrlsProvider){

    var color_thresholds = [0,9,24,49];

    function getMapColors(maps){
      return maps > color_thresholds[3] ? '#0033CC' :
             maps > color_thresholds[2] ? '#335CD6' :
             maps > color_thresholds[1] ? '#657FCB' :
             maps > color_thresholds[0] ? '#90A3D9' :
             'transparent'
    }

    angular.extend($scope, {
      layers: {
        baselayers: {
          ithaca: {
            name: 'ithaca-silver',
            type: 'wms',
            url: 'http://playground.ithacaweb.org/geoserver/gwc/service/wms',
            layerOptions: {
              layers: 'gmes:erds',
              format: 'image/png'
            }
          }
        }
      },
      center: {
        lat: 5.6,
        lng: 3.9,
        zoom: 2
      },
      legend: (function(){
        var colors = [0];
        for(var i=0; i<color_thresholds.length; i++){
          colors.push(getMapColors(color_thresholds[i]+1));
        }
        return {
          position: 'topright',
          colors: colors,
          labels: [ '<strong>Maps</strong>', '1 to 10', '10 to 25', '25 to 50', '50+']
        }
      })(),
    });

    var map = leafletData.getMap();

    var info_div = L.control({position: 'bottomleft'});
    
    info_div.onAdd = function(map){
      this._div = L.DomUtil.create('div', 'map_info');
      this.update();
      return this._div;
    };

    info_div.create_counts_snippet = function(counts){
      var html = '';
      for(var i=0; i < counts.length; i++){
        html += counts[i].category__name + ': ' + counts[i].count + '<br>';
      }
      return html;
    };

    info_div.update = function(country){
      this._div.innerHTML = country ? 
        '<p class="flag flag-' + country['iso3'].toLowerCase() + '"></p>' +
        '<strong>' + country['name'] + '</strong>' + 
        '<br><p class="map-info-counts">' + (country['maps_count']['total'] !== 0 ? 
          this.create_counts_snippet(country['maps_count']['counts']) : 
          'No maps') + '</p>':
        'Hover or click on a country';
    };

    map.then(function(map){
      info_div.addTo(map);
    });

    function styleCountry(feature) {
      return {
        weight: 0.2,
        opacity: 1,
        color: 'gray',
        fillOpacity: 0.7,
        fillColor: getMapColors(feature.maps_count.total)
      };
    }

    $http.get(UrlsProvider.country_url + '?limit=200&type=country').success(function(countries){
      angular.extend($scope, {
        countries: {
          data: {
            "type": "FeatureCollection",
            "features": countries.objects
          },
          style: styleCountry,
          onEachFeature: function(feature, layer){
            layer.on('mouseover', function(){
              info_div.update(feature);
            });
            layer.on('mouseout', function(){
              info_div.update();
            });
            layer.on('click', function(e){
              $scope.$emit('mapclicked', e.target.feature)
            });
          }
        }
      });
    });
  });
})();
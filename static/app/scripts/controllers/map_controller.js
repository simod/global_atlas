'use strict';

(function(){
  goog.provide('map_controller');

  var module = angular.module('map_controller', ['leaflet-directive']);

  module.controller('MapController', function($scope, $http, DataUrls,
   leafletData, UrlsProvider){
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
      }
    });

    var map = leafletData.getMap();

    var info_div = L.control({position: 'bottomleft'});
    
    info_div.onAdd = function(map){
      this._div = L.DomUtil.create('div', 'map_info');
      this.update();
      return this._div;
    };

    info_div.create_counts_snippet = function(maps_data){
      var html = '';
      for(var category in maps_data){
        if(maps_data[category] > 0 && category !== 'total'){
          html += category + ': ' + maps_data[category] + '<br>';
        }
      }
      return html;
    };

    info_div.update = function(country){
      this._div.innerHTML = country ? 
        '<p class="flag flag-' + country['iso3'].toLowerCase() + '"></p>' +
        '<strong>' + country['name'] + '</strong>' + 
        '<br><p class="map-info-counts">' + (country['maps_count']['total'] !== 0 ? 
          this.create_counts_snippet(country['maps_count']) : 
          'No maps') + '</p>':
        'Hover a country';
    };

    map.then(function(map){
      info_div.addTo(map);
    });

    function getMapColors(maps){
      return maps > 4 ? '#0033CC' :
             maps > 3 ? '#335CD6' :
             maps > 2 ? '#657FCB' :
             maps > 1 ? '#90A3D9' :
             maps > 0 ? '#66CCFF' :
             'transparent'
    }

    function styleCountry(feature) {
      return {
        weight: 0.5,
        opacity: 1,
        color: 'gray',
        fillOpacity: 0.7,
        fillColor: getMapColors(feature.maps_count.total)
      };
    }

    $http.get(UrlsProvider.country_url + '?limit=200').success(function(countries){
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
          }
        }
      });
    });
  });
})();
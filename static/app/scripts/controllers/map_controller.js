'use strict';

(function(){
  goog.provide('map_controller');

  var module = angular.module('map_controller', ['leaflet-directive']);

  module.controller('MapController', function($scope, $http, DataUrls, leafletData){
    angular.extend($scope, {
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

    info_div.update = function(country, maps_data){
      this._div.innerHTML = country ? '<strong>' + country['name'] + '</strong><br>' + 
        (maps_data ? this.create_counts_snippet(maps_data) : 'No maps') :
        'Hover a country';
    };

    map.then(function(map){
      info_div.addTo(map);
    });

    $http.get(DataUrls.countries).success(function(countries){
      $http.get(DataUrls.maps_count).success(function(maps_data){
        angular.extend($scope, {
          countries: {
            data: countries,
            style: {
              fillColor: 'grey',
              weight: 0.7,
              opacity: 1,
              color: 'white',
              fillOpacity: 0.9
            },
            onEachFeature: function(feature, layer){
              layer.on('mouseover', function(){
                info_div.update(feature.properties, maps_data[feature.id]);
              });
            }
          }
        });
      });
    });
  });
})();
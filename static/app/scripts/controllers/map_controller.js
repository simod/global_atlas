'use strict';

(function(){
  goog.provide('map_controller');

  var module = angular.module('map_controller', ['leaflet-directive']);

  module.controller('MapController', function($scope, $http, DataUrls){
    angular.extend($scope, {
      center: {
        lat: 5.6,
        lng: 3.9,
        zoom: 2
      }
    });
    $http.get(DataUrls.countries).success(function(data){
      angular.extend($scope, {
        countries: {
          data: data,
          style: {
            fillColor: 'grey',
            weight: 0.7,
            opacity: 1,
            color: 'white',
            fillOpacity: 0.9
          },
          onEachFeature: function(feature, layer){
            var popupContent = '<p>' + feature.properties.name + '</p>';

            layer.on('mouseover', function(){
              layer.bindPopup(popupContent, {
                feature: feature
              }).openPopup(layer.getBounds().getCenter());
            });
          }
        }
      });
    });
  });
})();
'use strict';

(function(){
  goog.provide('map_controller');

  var module = angular.module('map_controller', ['leaflet-directive']);

  module.controller('MapController', function($scope, $http,
   leafletData, UrlsProvider){

    function getMapColors(maps){
      return maps > 4 ? '#0033CC' :
             maps > 3 ? '#335CD6' :
             maps > 2 ? '#657FCB' :
             maps > 1 ? '#90A3D9' :
             maps > 0 ? '#66CCFF' :
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
        var colors = [];
        for(var i=0; i<6; i++){
          colors.push(getMapColors(i));
        }
        return {
          position: 'topright',
          colors: colors,
          labels: [ '<strong>Maps</strong>', 'One', 'Two', 'Three', 'Four', '4+']
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
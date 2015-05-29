'use strict';

(function(){
  goog.provide('map_controller');

  goog.require('atlas_search_service');

  var module = angular.module('map_controller', [
    'leaflet-directive',
    'atlas_search_service'
    ]);

  module.controller('MapController', function($scope, $http,
   leafletData, UrlsProvider, SearchService){
    var color_thresholds = [0,5,10,30];

    function getMapColors(maps){
      return maps > color_thresholds[3] ? 'rgb(68,101,137)' :
             maps > color_thresholds[2] ? 'rgb(102,153,205)' :
             maps > color_thresholds[1] ? 'rgb(158,187,215)' :
             maps > color_thresholds[0] ? 'rgb(190, 232,255)' :
             'transparent'
    }

    angular.extend($scope, {
      layers: {
        baselayers: {
          // ithaca: {
          //   name: 'stamen',
          //   type: 'xyz',
          //   url: 'http://{s}.tile.stamen.com/toner-lite/{z}/{x}/{y}.png'
          // },
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
        lat: 25,
        lng: 20,
        zoom: 3
      },
      legend: (function(){
        var colors = [0];
        for(var i=0; i<color_thresholds.length; i++){
          colors.push(getMapColors(color_thresholds[i]+1));
        }
        return {
          position: 'topright',
          colors: colors,
          labels: [ '<strong>Maps</strong>', '1 to 5', '6 to 10', '11 to 30', '30+']
        }
      })()
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
        html += counts[i].map__category__name + ': ' + counts[i].count + '<br>';
      }
      return html;
    };

    info_div.update = function(country){
      this._div.innerHTML = country ? 
        '<p class="flag flag-' + country['iso3'].toLowerCase() + '"></p>' +
        '<strong style="margin-right:10px;">' + country['name'] + '</strong>' + country['maps_count']['total'] +
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
              // On clik on a country, set the value in the select2
              // widget and seach
              $('#country_select').select2('data', 
                {id: feature.id, text: feature.name},true);
              SearchService.search();
            });
          }
        }
      });
    });
  });
})();
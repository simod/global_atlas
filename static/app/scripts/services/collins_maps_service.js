'use strict';
(function(){
  goog.provide('collins_maps_service');

  goog.require('atlas_url_provider');

  var module = angular.module('collins_maps_service', ['atlas_url_provider']);

  module.factory('CollinsMapsService', function($rootScope, $http, UrlsProvider){
    return {
      search: function(params){
        // by default the fix the id at 0 to get no maps
        var url = UrlsProvider.collins_url + 
        '?limit=20&country__id__in=0';

        return $http.get(url, {params: params});
        
      }
    }
  });
})();
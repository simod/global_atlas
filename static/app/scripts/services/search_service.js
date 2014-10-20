'use strict';
(function(){

  goog.provide('atlas_search_service');

  goog.require('atlas_url_provider');

  var module = angular.module('atlas_search_service', ['atlas_url_provider']);

  module.factory('SearchService', function($rootScope, $http, UrlsProvider){

   return {
      search: function(){
        var url_with_pagination = UrlsProvider.map_url + 
        '?limit=' + $rootScope.results_limit +
        '&offset=' + ($rootScope.results_limit * ($rootScope.page - 1)) + 
        '&order_by=-date';

        $http.get(url_with_pagination, {params: $rootScope.search_filters})
        .success(function(data){
          $rootScope.search_results = data.objects;
          $rootScope.search_total_counts = data.meta.total_count;
        });
      }
    }
  });
})();
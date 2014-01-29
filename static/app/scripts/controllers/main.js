'use strict';
(function(){
  goog.provide('atlas_main_controller');

  goog.require('atlas_url_provider');

  var module = angular.module('atlas_main_controller', ['atlas_url_provider']);

  module.controller('AtlasController', function ($scope, $http, UrlsProvider) {
    
    $scope.search_filters = {};

    // Update the filters on change of the country selections
    $('#country_select').on('change', function(e){
      $scope.search_filters['country__id__in'] = e.val;
    });


    // React to the change of the filters and trigger the search
    $scope.$watch('search_filters', function(newVal, oldVal){
      search();
    },true);

    function search(){
      $http.get(UrlsProvider.map_url, {params: $scope.search_filters})
      .success(function(data){
        $scope.search_results = data.objects;
      });
    }
  });
})();
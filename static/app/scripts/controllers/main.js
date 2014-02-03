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

    // Listed to the map click event and set the country filter
    $scope.$on('mapclicked', function(e, feature){
      $('#country_select').select2('data', 
        {id: feature.id, text: feature.name}, 
        true);
    });

    // Manage the search filters
    $('.search_filter').find('li').click(function(e){

      if($(e.target).hasClass('active')){
        // clear active classes in the parent block
        $(e.target).parent().find('li').removeClass('active');

        // Remove the filters entry
        delete $scope.search_filters[$(e.target)
        .attr('data-class') + '__id'];        
      }
      else{
        // clear active classes in the parent block
        $(e.target).parent().find('li').removeClass('active');

        //Add the active class
        $(e.target).addClass('active');

        // Add the entry in the filters
        $scope.search_filters[$(e.target)
          .attr('data-class') + '__id'] = $(e.target).val();
      }
      // Trigger the scope digest
      $scope.$digest();
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
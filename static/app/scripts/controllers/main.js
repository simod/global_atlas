'use strict';
(function(){
  goog.provide('atlas_main_controller');

  goog.require('atlas_url_provider');
  goog.require('atlas_search_service');

  var module = angular.module('atlas_main_controller', [
    'atlas_url_provider',
    'atlas_search_service'
    ]);

  module.controller('AtlasController', function (
    $scope, $http, $rootScope, UrlsProvider, SearchService
  ) {

    $rootScope.page = 1;
    $rootScope.results_limit = 5;
    $rootScope.search_filters = {};
    $rootScope.search_results = [];
    $rootScope.search_total_counts = 0;
    $rootScope.numpages = 1;

    // Control what happens when the total results change
    $scope.$watch('search_total_counts', function(){
      $rootScope.numpages = Math.round(
        ($rootScope.search_total_counts / $rootScope.results_limit) + 0.49
      );

      // In case the user is viewing a page > 1 and a 
      // subsequent query returns less pages, then 
      // reset the page to one and search again.
      if($rootScope.numpages < $rootScope.page){
        $rootScope.page = 1;
        SearchService.search();
      }

      // In case of no results, the number of pages is one.
      if($rootScope.numpages == 0){$rootScope.numpages = 1};
    });

    $scope.reset_filters = function(){
      $rootScope.search_filters = [];
      $('#country_select').select2('val', '', true);
      $('.search_filter').find('li').removeClass('active');
      $('#title_search').val('');
      SearchService.search();
    }

    $scope.paginate_down = function(){
      if($rootScope.page > 1){
        $rootScope.page -= 1;
        SearchService.search();
      }   
    }

    $scope.paginate_up = function(){
      if($rootScope.numpages > $rootScope.page){
        $rootScope.page += 1;
        SearchService.search();
      }
    }
  });
})();
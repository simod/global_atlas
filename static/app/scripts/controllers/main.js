'use strict';
(function(){
  goog.provide('atlas_main_controller');

  goog.require('atlas_url_provider');

  var module = angular.module('atlas_main_controller', ['atlas_url_provider']);

  module.controller('AtlasController', function ($scope, $http, UrlsProvider) {
    $scope.page = 1;
    $scope.results_limit = 5;
    $scope.search_filters = {};
    $scope.search_results = [];
    $scope.search_total_counts = 0;
    $scope.numpages = 1;

    $scope.$watch('search_total_counts', function(){
      $scope.numpages = Math.round(
        ($scope.search_total_counts / $scope.results_limit) + 0.49
      );
      if($scope.numpages == 0){$scope.numpages =1};
    });

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

    // Listen to the title change and query
    $scope.$on('query_by_title', function(e, title){
      $scope.search_filters['title__icontains'] = title;
      search();
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

    $scope.paginate_down = function(){
      if($scope.page > 1){
        $scope.page -= 1;
        search();
      }   
    }

    $scope.paginate_up = function(){
      if($scope.numpages > $scope.page){
        $scope.page += 1;
        search();
      }
    }

    function search(){
      var url_with_pagination = UrlsProvider.map_url + 
        '?limit=' + $scope.results_limit +
        '&offset=' + ($scope.results_limit * ($scope.page - 1));

      $http.get(url_with_pagination, {params: $scope.search_filters})
      .success(function(data){
        $scope.search_results = data.objects;
        $scope.search_total_counts = data.meta.total_count;
      });
    }
  });
})();
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

    // Control what happens when the total results change
    $scope.$watch('search_total_counts', function(){
      $scope.numpages = Math.round(
        ($scope.search_total_counts / $scope.results_limit) + 0.49
      );

      // In case the user is viewing a page > 1 and a 
      // subsequent query returns less pages, then 
      // reset the page to one and search again.
      if($scope.numpages < $scope.page){
        $scope.page = 1;
        search();
      }

      // In case of no results, the number of pages is one.
      if($scope.numpages == 0){$scope.numpages = 1};
    });

    // Update the filters on change of the country selections
    $('#country_select').on('change', function(e){
      $scope.search_filters['country__id__in'] = e.val;
      search();
    });

    // Listed to the map click event and set the country filter
    $scope.$on('mapclicked', function(e, feature){
      $('#country_select').select2('data', 
        {id: feature.id, text: feature.name},true);
      search();
    });

    // Listen to the title change and set the title filter
    $scope.$on('query_by_title', function(e, title){
      if(isNaN(parseInt(title))){
        $scope.search_filters['title__icontains'] = title;
      }else{
        $scope.search_filters['id__contains'] = title;
      }
      search();
    });

    // Manage the search filters lists adding and removing
    // the 'active' class ad the id in the relative search filter 
    $('.search_filter').find('li').click(function(e){

      // if is active enter the deactivate block
      if($(e.target).hasClass('active')){

        // is single choice
        if(!$(e.target).parent().hasClass('multiple_choice')){
          // clear all acrive classes for the block
          $(e.target).parent().find('li').removeClass('active');
          // Remove the filters entry
          delete $scope.search_filters[$(e.target)
            .attr('data-class') + '__id'];    
        }
        else // is a multiple choice
        {
          // get the correct filter
          var filter = $scope.search_filters[$(e.target)
            .attr('data-class') + '__id__in'];
          // remove just the correct entry from the filter array
          $(e.target).removeClass('active');
            filter.splice(filter.indexOf($(e.target).val()),1);         
        }               
      }
      else // is not active, then activate
      {
        // is single choice
        if(!$(e.target).parent().hasClass('multiple_choice')){
          // clear all active classes for the block
          $(e.target).parent().find('li').removeClass('active');
          // Add the filters entry
          $scope.search_filters[$(e.target)
            .attr('data-class') + '__id'] = $(e.target).val();
        }
        else // is a multiple choice
        {
          // get the correct filter
          var filter = $scope.search_filters[$(e.target)
            .attr('data-class') + '__id__in'];
          // Add the correct entry in the filters array
          filter.push($(e.target).val());
        }
        //Add the active class
        $(e.target).addClass('active');        
      }
      // Search
      search();
    });

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
'use strict';

(function(){

  goog.provide('title_select_controller');

  goog.require('atlas_search_service');

  var module = angular.module('title_select_controller',['atlas_search_service']);

  module.controller('TitleSelectController', function($scope, $rootScope, SearchService){
    $scope.title = '';
    $scope.$watch('title', function(){
      if(isNaN(parseInt($scope.title))){
        $rootScope.search_filters['title__icontains'] = $scope.title;
        delete $rootScope.search_filters['id__exact'];
      }else{
        $rootScope.search_filters['id__exact'] = $scope.title;
        delete $rootScope.search_filters['title__icontains'];
      }
      SearchService.search();
    });
  });
})();
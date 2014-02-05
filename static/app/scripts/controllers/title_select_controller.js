'use strict';

(function(){

  goog.provide('title_select_controller');

  var module = angular.module('title_select_controller',[]);

  module.controller('TitleSelectController', function($scope){
    $scope.title = '';
    $scope.$watch('title', function(){
      $scope.$emit('query_by_title', $scope.title);
    })
  });
})();
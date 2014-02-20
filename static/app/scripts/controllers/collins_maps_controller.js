'use strict';
(function(){
  goog.provide('collins_maps_controller');

  goog.require('collins_maps_service');

  var module = angular.module('collins_maps_controller', ['collins_maps_service']);

  module.controller('CollinsMapsController', function($scope, $rootScope, CollinsMapsService){
    $scope.collins_maps = [];
    $scope.$on('country_changed', function(event, params){
      CollinsMapsService.search(params).success(function(data){
        $scope.collins_maps = data.objects;
      });
    });
  });
})();
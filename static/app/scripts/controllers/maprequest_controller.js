'use strict';

(function(){
  goog.provide('atlas_mr_controller');

  goog.require('atlas_url_provider');


  var module = angular.module('atlas_mr_controller', ['atlas_url_provider']);

  module.controller('MRController', function($scope, UrlsProvider){
    
    $scope.submit = function(){
      UrlsProvider.request_post({
        title: $scope.title,
        email: $scope.email,
        purpose: $scope.purpose,
        extended_description: $scope.extended_description,
        content: $scope.content,
        deadline: $scope.deadline,
        size: UrlsProvider.size_url + $scope.size +'/',
        format: UrlsProvider.format_url + $scope.format +'/',
        requester: UrlsProvider.requester_url + $scope.requester +'/'
      });
    }
  });

})();
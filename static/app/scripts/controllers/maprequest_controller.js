'use strict';

(function(){
  goog.provide('atlas_mr_controller');

  goog.require('atlas_url_provider');


  var module = angular.module('atlas_mr_controller', ['atlas_url_provider']);

  module.controller('MRController', function($scope, UrlsProvider){
    
    $scope.email = 'your@email.com';

    $scope.submit = function(){
      UrlsProvider.request_post({email:$scope.email});
    }
  });

})();
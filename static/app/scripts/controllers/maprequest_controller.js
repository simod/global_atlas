'use strict';

(function(){
  goog.provide('atlas_mr_controller');

  goog.require('atlas_url_provider');


  var module = angular.module('atlas_mr_controller', ['atlas_url_provider']);

  module.controller('MRController', function($scope, $http, UrlsProvider){
    $scope.submit = function(){

      var data = {
        title: $scope.title,
        email: $scope.email,
        purpose: $scope.purpose,
        extended_description: $scope.extended_description,
        content: $scope.content,
        deadline: $scope.deadline,
        size: UrlsProvider.size_url + $scope.size +'/',
        format: UrlsProvider.format_url + $scope.format +'/',
        requester: UrlsProvider.requester_url + $scope.requester +'/'
      }

      $http.post(UrlsProvider.request_url, data)
        .success(function(data, status, headers, config){
          $('#mr_form').modal('toggle');
          alert('Your request is correctly registered!');
        })
        .error(function(data, status, headers, config){
          alert(data['error']);
        });
    }
  });
})();
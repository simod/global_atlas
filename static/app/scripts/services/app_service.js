'use strict';
(function(){
  goog.provide('atlas_app_service');

  var module = angular.module('atlas_app_service', ['ngResource']);

  module.factory('ApiUrls', function($resource, atlasSettings){
    return $resource(atlasSettings.api_endpoint, {}, {
      query: {method:'GET'}
    });
  });
})();
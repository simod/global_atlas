'use strict';
(function(){
  goog.provide('atlas_main_controller');

  goog.require('atlas_app_service');

  var module = angular.module('atlas_main_controller',['atlas_app_service']);

  module.controller('AtlasController', function ($scope, ApiUrls) {
    console.log('controller');
    console.log(ApiUrls.query());
  });
})();
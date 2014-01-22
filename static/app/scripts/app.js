'use strict';
(function(){
  goog.provide('atlas');

  goog.require('atlas_main_controller');
  goog.require('atlas_mr_controller');

  var module = angular.module('atlas', [
    'ngCookies',
    'ngResource',
    'ngSanitize',
    'ngRoute',
    'atlas_main_controller',
    'atlas_mr_controller'
  ]);
})(); 
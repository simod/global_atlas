'use strict';
(function(){
  goog.provide('atlas');

  goog.require('atlas_main_controller');
  goog.require('atlas_mr_controller');
  goog.require('country_select_controller');
  goog.require('title_select_controller');
  goog.require('map_controller');
  goog.require('single_choice_service');
  goog.require('single_choice_directive');


  var module = angular.module('atlas', [
    'atlas_main_controller',
    'atlas_mr_controller',
    'country_select_controller',
    'title_select_controller',
    'map_controller',
    'single_choice_service',
    'single_choice_directive'
  ]);
})(); 
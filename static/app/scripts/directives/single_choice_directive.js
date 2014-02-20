'use strict';
(function(){
  goog.provide('single_choice_directive');

  goog.require('single_choice_service');

  var module = angular.module('single_choice_directive',['single_choice_service']);

  // Attach a listener on the songle choice divs adding a single choice logic
  module.directive('singleChoiceDirective', function(SingleChoiceFactory){
    return {
      restrict: 'A',
      link: function(scope, element, attrs){
        $(element[0]).find('li').click(SingleChoiceFactory.handleSingleChoiceFilters);
      }
    }
  });
})();
'use strict';
(function(){
  goog.provide('single_choice_service');

  goog.require('atlas_search_service');

  var module = angular.module('single_choice_service', ['atlas_search_service']);

  // Manage the single choice search filters lists adding and removing
  // the 'active' class ad the id in the relative search filter
  module.factory('SingleChoiceFactory', function($rootScope, SearchService){
    return {
      handleSingleChoiceFilters: function(e){    
        // If active then deactivate it
        if($(e.target).hasClass('active')){
          // clear all active classes for the block
          $(e.target).parents('ul').find('li').removeClass('active');
          // Remove the filters entry
          delete $rootScope.search_filters[$(e.target)
            .attr('data-class') + '__id']; 
        }
        else if(!$(e.target).hasClass('active')){
          // clear all active classes for the block
          $(e.target).parents('ul').find('li').removeClass('active');
          // Add the filters entry
          $rootScope.search_filters[$(e.target)
            .attr('data-class') + '__id'] = $(e.target).val();
            
          // If is a region then clean the country selection
          if($(e.target).attr('data-class') === 'country'){
            $('#country_select').select2('val', '');
            delete $rootScope.search_filters['country__id__in'];
          }
          $(e.target).addClass('active');
        }
        SearchService.search();
      }
    }
  });
})();
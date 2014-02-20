'use strict';

(function(){

  goog.provide('country_select_controller');

  goog.require('atlas_url_provider');
  goog.require('atlas_search_service');

  var module = angular.module('country_select_controller',[
    'ui.select2'
    ]);

  module.controller('CountrySelectController', function(
    $scope, $rootScope, UrlsProvider, SearchService){

    $scope.select2Options = {
      minimumInputLength: 1,
      width: '150px',
      multiple: true,
      tags: [],
      ajax: {
        url: UrlsProvider.country_url + '?type=country',
        data: function(q){
          return {
            q: q
          }
        },
        results: function(data) {
          return {
            results: $.map(data.objects,function(object){
              return {id: object.id, text: object.name, fips: object.fips};
            })
          }
        }
      },
      initSelection: function (element, callback) {
        callback(element.val());
      }
    };

    // Update the filters on change of the country selections
    $('#country_select').on('change', function(e){
      $rootScope.search_filters['country__id__in'] = e.val;
      // clean any region filter
      $('.search_filter').find('[data-class="country"]').removeClass('active');
      delete $rootScope.search_filters['country__id'];
      SearchService.search();
      $rootScope.$broadcast('country_changed', {'country__id__in': e.val});
    });
  });
})();
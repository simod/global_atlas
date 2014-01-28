'use strict';

(function(){

  goog.provide('country_select_controller');

  goog.require('atlas_url_provider');

  var module = angular.module('country_select_controller',['ui.select2']);

  module.controller('CountrySelectController', function($scope, UrlsProvider){

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
      }
    }
  });
})();
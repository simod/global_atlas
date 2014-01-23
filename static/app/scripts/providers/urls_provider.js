'use strict';

/*
* Provides the backend api communication connections
*/

(function(){
  goog.provide('atlas_url_provider');

  var module = angular.module('atlas_url_provider', []);

  module.provider('UrlsProvider', function(){

    this.$get = ['$http', 'ApiUrls', function($http, ApiUrls){

      return {
        request_post: function(data){
          $http.post(ApiUrls.urls.requests.list_endpoint, data)
            .success(function(){
              alert('Success');
            })
            .error(function(){
              alert('error');
            });
        }
      }

    }]

  });
})();